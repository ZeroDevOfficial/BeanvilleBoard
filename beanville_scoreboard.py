import os
import yaml
import time
import threading
from endstone.plugin import Plugin
from endstone.event import event_handler, PlayerJoinEvent, PlayerQuitEvent
from endstone.scoreboard import DisplaySlot, ObjectiveSortOrder, Criteria
from endstone.boss import BossBar, BarColor, BarStyle

class BeanvilleBoard(Plugin):
    api_version = "0.5"

    def on_enable(self):
        self.logger.info("Beanville Scoreboard and BossBar System Activated.")
        self.sb = self.server.scoreboard
        self.is_running = True
        
        # Core dynamic tracker metrics variables
        self.current_player_line = ""
        self.current_death_line = ""
        self.current_day_line = ""
        self.current_welcome_line = ""
        
        self.global_deaths_today = 0
        self.tracked_minecraft_day = 0
        
        # Color shifting parameters
        self.rainbow_index = 0
        self.rainbow_colors = ["§c", "§6", "§e", "§a", "§b", "§d"] # Red, Gold, Yellow, Green, Aqua, Pink
        self.dead_players = set()
        self.bar_progress_value = 0.0
        
        # Automatically read or generate configuration configurations
        self.load_plugin_config()
        
        # Initialize the Core BossBar Instance using config defaults
        try:
            color_enum = getattr(BarColor, self.cfg_bar_color.upper(), BarColor.PURPLE)
            style_enum = getattr(BarStyle, self.cfg_bar_style.upper(), BarStyle.SOLID)
        except Exception:
            color_enum = BarColor.PURPLE
            style_enum = BarStyle.SOLID

        self.boss_bar = self.server.create_boss_bar(
            self.cfg_bossbar_title, 
            color_enum, 
            style_enum
        )
        self.boss_bar.progress = 0.0
        
        # Build initial board data on boot
        self.update_live_data()
        
        # Stable main-thread update trigger interval task loop
        self.loop_exit_flag = threading.Event()
        threading.Thread(target=self.start_safe_ticker_loop, daemon=True).start()

    def load_plugin_config(self):
        """Generates or pulls configurations straight out of the server profile folder."""
        config_dir = os.path.join("plugins", "BeanvilleBoard")
        config_file = os.path.join(config_dir, "config.yml")
        
        default_config = {
            "bossbar-title": "§d§l> Beanville 2.0 <§r",
            "bossbar-color": "PURPLE",
            "bossbar-style": "SOLID",
            "scoreboard-title": "§d§l> Beanville 2.0 <§r",
            "welcome-text": "Welcome Friends!"
        }
        
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            
        if not os.path.exists(config_file):
            with open(config_file, "w", encoding="utf-8") as f:
                yaml.dump(default_config, f, default_flow_style=False)
                
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f) or default_config
        except Exception:
            loaded = default_config
            
        self.cfg_bossbar_title = loaded.get("bossbar-title", "§d§l> Beanville 2.0 <§r")
        self.cfg_bar_color = loaded.get("bossbar-color", "PURPLE")
        self.cfg_bar_style = loaded.get("bossbar-style", "SOLID")
        self.cfg_sb_title = loaded.get("scoreboard-title", "§d§l> Beanville 2.0 <§r")
        self.cfg_welcome = loaded.get("welcome-text", "Welcome Friends!")

    def start_safe_ticker_loop(self):
        """Ticks exactly every 1.0 second cleanly without stack memory risks."""
        while not self.loop_exit_flag.wait(1.0):
            if not self.is_running:
                break
            try:
                self.server.scheduler.run_task(self, self.update_live_data)
            except Exception:
                pass

    def update_live_data(self):
        if not self.is_running:
            return

        # 1. Direct Health Check Loop
        for player in self.server.online_players:
            if player.health <= 0:
                if player.name not in self.dead_players:
                    self.global_deaths_today += 1
                    self.dead_players.add(player.name)
            else:
                if player.name in self.dead_players:
                    self.dead_players.remove(player.name)

        # 2. Day Counter and Auto-Reset Mechanic
        current_time = self.server.level.time
        mc_day = int(current_time / 24000) + 1
        
        if mc_day != self.tracked_minecraft_day:
            self.tracked_minecraft_day = mc_day
            self.global_deaths_today = 0

        # 3. Rainbow Color Step Logic
        current_color = self.rainbow_colors[self.rainbow_index]
        welcome_line = f"{current_color}{self.cfg_welcome}§r"
        
        # 4. Smooth Loading Animation Loop (0% -> 100%) and Auto-Packet Handshake
        if hasattr(self, 'boss_bar') and self.boss_bar:
            clean_title = self.cfg_bossbar_title.replace("§d", current_color).replace("§l", "§l")
            self.boss_bar.title = clean_title
            
            # Increment loading progress value by 5% each interval tick
            self.bar_progress_value += 0.05
            if self.bar_progress_value > 1.0:
                self.bar_progress_value = 0.0 
                
            self.boss_bar.progress = self.bar_progress_value
            
            # Re-verify and cycle packets to force rendering immediately after chunk screens clear
            for player in self.server.online_players:
                try:
                    if player in self.boss_bar.players:
                        self.boss_bar.remove_player(player)
                    self.boss_bar.add_player(player)
                except Exception:
                    pass
        
        self.rainbow_index = (self.rainbow_index + 1) % len(self.rainbow_colors)

        # 5. Compile scoreboard string data
        online_count = len(self.server.online_players)
        players_line = f"§bPlayers:§r §6{online_count}/{self.server.max_players}§r"
        day_line = f"§eDay:§r §f{self.tracked_minecraft_day}§r"
        deaths_line = f"§cDeaths Today:§r §f{self.global_deaths_today}§r"
        
        # 6. Redraw objective display only if metric data points shift
        if (players_line != self.current_player_line or 
            deaths_line != self.current_death_line or 
            day_line != self.current_day_line or
            welcome_line != self.current_welcome_line):
            
            old_objective = self.sb.get_objective("b_side")
            if old_objective:
                old_objective.unregister()
                
            self.objective = self.sb.add_objective(
                name="b_side", 
                criteria=Criteria.Type.DUMMY, 
                display_name=self.cfg_sb_title
            )
            
            self.objective.set_display(DisplaySlot.SIDE_BAR, ObjectiveSortOrder.ASCENDING)
            
            # Fixed grid mapping order layout numbers
            self.objective.get_score(welcome_line).value = 4
            self.objective.get_score(deaths_line).value = 3
            self.objective.get_score(day_line).value = 2
            self.objective.get_score(players_line).value = 1
            
            self.current_player_line = players_line
            self.current_death_line = deaths_line
            self.current_day_line = day_line
            self.current_welcome_line = welcome_line

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        if hasattr(self, 'boss_bar') and self.boss_bar:
            try:
                self.boss_bar.add_player(event.player)
            except Exception:
                pass
        self.update_live_data()

    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent):
        if event.player.name in self.dead_players:
            self.dead_players.remove(event.player.name)
        self.update_live_data()

    def on_disable(self):
        self.is_running = False
        if hasattr(self, 'loop_exit_flag'):
            self.loop_exit_flag.set() # Safely shut down background thread actions
        if hasattr(self, 'boss_bar') and self.boss_bar:
            try:
                for player in list(self.boss_bar.players):
                    self.boss_bar.remove_player(player)
            except Exception:
                pass
        old_objective = self.sb.get_objective("b_side")
        if old_objective:
            try:
                old_objective.unregister()
            except Exception:
                pass
