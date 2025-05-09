import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import sys
import subprocess


class BSESettingsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bristol Stock Exchange Settings")
        self.root.geometry("650x500")

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create tabs
        self.general_tab = ttk.Frame(self.notebook)
        self.traders_tab = ttk.Frame(self.notebook)
        self.output_tab = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.general_tab, text="Simulation")
        self.notebook.add(self.traders_tab, text="Traders")
        self.notebook.add(self.output_tab, text="Output")

        # Set up the tabs
        self.setup_general_tab()
        self.setup_traders_tab()
        self.setup_output_tab()

        # Add control buttons at the bottom
        self.setup_control_buttons()

        # Load default settings
        self.load_default_settings()

    def setup_general_tab(self):
        frame = ttk.LabelFrame(self.general_tab, text="Simulation Parameters")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Simulation duration
        ttk.Label(frame, text="Simulation Duration (days):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.n_days_var = tk.DoubleVar()
        self.n_days_slider = ttk.Scale(frame, from_=0.01, to=10.0, orient=tk.HORIZONTAL,
                                       variable=self.n_days_var, length=300)
        self.n_days_slider.grid(row=0, column=1, padx=10, pady=5)
        self.n_days_entry = ttk.Entry(frame, width=10, textvariable=self.n_days_var)
        self.n_days_entry.grid(row=0, column=2, padx=10, pady=5)

        # Hours per day
        ttk.Label(frame, text="Hours per day:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.hours_var = tk.DoubleVar()

        self.hours_slider = ttk.Scale(
            frame,
            from_=0.5,
            to=24.0,
            orient=tk.HORIZONTAL,
            variable=self.hours_var,
            length=300,
            command=lambda v: self.hours_var.set(round(float(v) * 2) / 2)  # Round to nearest 0.5
        )
        self.hours_slider.grid(row=1, column=1, padx=10, pady=5)
        self.hours_entry = ttk.Entry(frame, width=10, textvariable=self.hours_var)
        self.hours_entry.grid(row=1, column=2, padx=10, pady=5)

        # Number of trials
        ttk.Label(frame, text="Number of trials:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.n_trials_var = tk.IntVar()
        self.n_trials_slider = ttk.Scale(frame, from_=1, to=100, orient=tk.HORIZONTAL,
                                         variable=self.n_trials_var, length=300)
        self.n_trials_slider.grid(row=2, column=1, padx=10, pady=5)
        self.n_trials_entry = ttk.Entry(frame, width=10, textvariable=self.n_trials_var)
        self.n_trials_entry.grid(row=2, column=2, padx=10, pady=5)

        # Number of recorded trials
        ttk.Label(frame, text="Number of recorded trials:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.n_recorded_var = tk.IntVar()
        self.n_recorded_slider = ttk.Scale(frame, from_=1, to=100, orient=tk.HORIZONTAL,
                                           variable=self.n_recorded_var, length=300)
        self.n_recorded_slider.grid(row=3, column=1, padx=10, pady=5)
        self.n_recorded_entry = ttk.Entry(frame, width=10, textvariable=self.n_recorded_var)
        self.n_recorded_entry.grid(row=3, column=2, padx=10, pady=5)

        # Verbose output checkbox
        self.verbose_var = tk.BooleanVar()
        self.verbose_check = ttk.Checkbutton(frame, text="Verbose output", variable=self.verbose_var)
        self.verbose_check.grid(row=5, column=0, sticky="w", padx=10, pady=5)

    def setup_traders_tab(self):
        frame = ttk.LabelFrame(self.traders_tab, text="Trader Configurations")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Trader types
        trader_types = ["GVWY", "SHVR", "ZIC", "ZIP", "PRZI", "PRSH", "PRDE"]

        # Buyer section
        buyer_frame = ttk.LabelFrame(frame, text="Buyers")
        buyer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(buyer_frame, text="Type").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(buyer_frame, text="Count").grid(row=0, column=1, padx=5, pady=5)

        self.buyer_types = []
        self.buyer_counts = []

        for i in range(5):  # Allow up to 5 different buyer types
            type_var = tk.StringVar()
            count_var = tk.IntVar()

            trader_combo = ttk.Combobox(buyer_frame, values=trader_types, textvariable=type_var, width=6)
            trader_combo.grid(row=i + 1, column=0, padx=5, pady=2)

            count_entry = ttk.Entry(buyer_frame, width=5, textvariable=count_var)
            count_entry.grid(row=i + 1, column=1, padx=5, pady=2)

            self.buyer_types.append(type_var)
            self.buyer_counts.append(count_var)

        # Seller section
        seller_frame = ttk.LabelFrame(frame, text="Sellers")
        seller_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(seller_frame, text="Type").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(seller_frame, text="Count").grid(row=0, column=1, padx=5, pady=5)

        self.seller_types = []
        self.seller_counts = []

        for i in range(5):  # Allow up to 5 different seller types
            type_var = tk.StringVar()
            count_var = tk.IntVar()

            trader_combo = ttk.Combobox(seller_frame, values=trader_types, textvariable=type_var, width=6)
            trader_combo.grid(row=i + 1, column=0, padx=5, pady=2)

            count_entry = ttk.Entry(seller_frame, width=5, textvariable=count_var)
            count_entry.grid(row=i + 1, column=1, padx=5, pady=2)

            self.seller_types.append(type_var)
            self.seller_counts.append(count_var)

        # Use same traders checkbox
        self.same_traders_var = tk.BooleanVar()
        self.same_traders_check = ttk.Checkbutton(
            frame,
            text="Use same configuration for buyers and sellers",
            variable=self.same_traders_var,
            command=self.toggle_same_traders
        )
        self.same_traders_check.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)

    def toggle_same_traders(self):
        """Copy buyer settings to seller settings when checkbox is checked"""
        if self.same_traders_var.get():
            for i in range(len(self.buyer_types)):
                self.seller_types[i].set(self.buyer_types[i].get())
                self.seller_counts[i].set(self.buyer_counts[i].get())

    def setup_output_tab(self):
        frame = ttk.LabelFrame(self.output_tab, text="Output Settings")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Checkboxes for output files
        self.dump_blotters_var = tk.BooleanVar()
        self.dump_blotters_check = ttk.Checkbutton(frame, text="Dump blotters", variable=self.dump_blotters_var)
        self.dump_blotters_check.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.dump_lobs_var = tk.BooleanVar()
        self.dump_lobs_check = ttk.Checkbutton(frame, text="Dump LOBs", variable=self.dump_lobs_var)
        self.dump_lobs_check.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.dump_strats_var = tk.BooleanVar()
        self.dump_strats_check = ttk.Checkbutton(frame, text="Dump strategies", variable=self.dump_strats_var)
        self.dump_strats_check.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.dump_avgbals_var = tk.BooleanVar()
        self.dump_avgbals_check = ttk.Checkbutton(frame, text="Dump average balances", variable=self.dump_avgbals_var)
        self.dump_avgbals_check.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.dump_tape_var = tk.BooleanVar()
        self.dump_tape_check = ttk.Checkbutton(frame, text="Dump tape", variable=self.dump_tape_var)
        self.dump_tape_check.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        # Output directory
        ttk.Label(frame, text="Output directory:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.output_dir_var = tk.StringVar()
        self.output_dir_entry = ttk.Entry(frame, width=50, textvariable=self.output_dir_var)
        self.output_dir_entry.grid(row=5, column=1, sticky="w", padx=10, pady=5)
        self.output_dir_button = ttk.Button(frame, text="Browse...", command=self.select_output_dir)
        self.output_dir_button.grid(row=5, column=2, sticky="w", padx=10, pady=5)

    def select_output_dir(self):
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.output_dir_var.set(directory)

    def setup_control_buttons(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)

        # Add buttons for save, load, reset, run
        self.save_button = ttk.Button(button_frame, text="Save Settings", command=self.save_settings)
        self.save_button.pack(side="left", padx=5)

        self.load_button = ttk.Button(button_frame, text="Load Settings", command=self.load_settings)
        self.load_button.pack(side="left", padx=5)

        self.reset_button = ttk.Button(button_frame, text="Reset to Defaults", command=self.load_default_settings)
        self.reset_button.pack(side="left", padx=5)

        self.run_button = ttk.Button(button_frame, text="Apply & Run Simulation", command=self.run_simulation)
        self.run_button.pack(side="right", padx=5)

        self.apply_button = ttk.Button(button_frame, text="Apply Settings", command=self.apply_settings)
        self.apply_button.pack(side="right", padx=5)

    def load_default_settings(self):
        # General settings
        self.n_days_var.set(0.01)
        self.hours_var.set(24.0)
        self.n_trials_var.set(1)
        self.n_recorded_var.set(1)
        self.verbose_var.set(False)

        # Trader settings
        default_buyers = [("SHVR", 5), ("GVWY", 5), ("ZIC", 2), ("ZIP", 13)]
        for i, (type_var, count_var) in enumerate(zip(self.buyer_types, self.buyer_counts)):
            if i < len(default_buyers):
                type_var.set(default_buyers[i][0])
                count_var.set(default_buyers[i][1])
            else:
                type_var.set("")
                count_var.set(0)

        self.same_traders_var.set(True)
        self.toggle_same_traders()

        # Output settings
        self.dump_blotters_var.set(True)
        self.dump_lobs_var.set(False)
        self.dump_strats_var.set(True)
        self.dump_avgbals_var.set(True)
        self.dump_tape_var.set(True)
        self.output_dir_var.set(os.getcwd())

    def save_settings(self):
        """Save current settings to a JSON file"""
        settings = self.collect_settings()

        # Ask user for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save BSE Settings",
            initialfile="settings"
        )

        if not filename:
            return

        try:
            with open(filename, 'w') as f:
                json.dump(settings, f, indent=4)
            messagebox.showinfo("Success", f"Settings saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def load_settings(self):
        """Load settings from a JSON file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load BSE Settings"
        )

        if not filename:
            return

        try:
            with open(filename, 'r') as f:
                settings = json.load(f)

            self.apply_loaded_settings(settings)
            messagebox.showinfo("Success", f"Settings loaded from {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {str(e)}")

    def apply_loaded_settings(self, settings):
        """Apply loaded settings to the GUI"""
        # General settings
        self.n_days_var.set(settings.get("n_days", 0.01))
        self.hours_var.set(settings.get("hours_in_a_day", 24.0))
        self.n_trials_var.set(settings.get("n_trials", 1))
        self.n_recorded_var.set(settings.get("n_trials_recorded", 1))
        self.verbose_var.set(settings.get("verbose", False))

        # Trader settings
        buyers = settings.get("buyers_spec", [])
        for i, (type_var, count_var) in enumerate(zip(self.buyer_types, self.buyer_counts)):
            if i < len(buyers):
                type_var.set(buyers[i][0])
                count_var.set(buyers[i][1])
            else:
                type_var.set("")
                count_var.set(0)

        sellers = settings.get("sellers_spec", [])
        for i, (type_var, count_var) in enumerate(zip(self.seller_types, self.seller_counts)):
            if i < len(sellers):
                type_var.set(sellers[i][0])
                count_var.set(sellers[i][1])
            else:
                type_var.set("")
                count_var.set(0)

        self.same_traders_var.set(settings.get("same_traders", True))

        # Output settings
        dump_flags = settings.get("dump_flags", {})
        self.dump_blotters_var.set(dump_flags.get("dump_blotters", True))
        self.dump_lobs_var.set(dump_flags.get("dump_lobs", False))
        self.dump_strats_var.set(dump_flags.get("dump_strats", True))
        self.dump_avgbals_var.set(dump_flags.get("dump_avgbals", True))
        self.dump_tape_var.set(dump_flags.get("dump_tape", True))
        self.output_dir_var.set(settings.get("output_dir", os.getcwd()))

    def collect_settings(self):
        """Collect all settings into a dictionary"""
        settings = {}

        # General settings
        settings["n_days"] = self.n_days_var.get()
        settings["hours_in_a_day"] = self.hours_var.get()
        settings["n_trials"] = self.n_trials_var.get()
        settings["n_trials_recorded"] = self.n_recorded_var.get()
        settings["verbose"] = self.verbose_var.get()

        # Trader settings
        buyers_spec = []
        for type_var, count_var in zip(self.buyer_types, self.buyer_counts):
            ttype = type_var.get()
            count = count_var.get()
            if ttype and count > 0:
                buyers_spec.append((ttype, count))
        settings["buyers_spec"] = buyers_spec

        sellers_spec = []
        for type_var, count_var in zip(self.seller_types, self.seller_counts):
            ttype = type_var.get()
            count = count_var.get()
            if ttype and count > 0:
                sellers_spec.append((ttype, count))
        settings["sellers_spec"] = sellers_spec

        settings["same_traders"] = self.same_traders_var.get()

        # Output settings
        dump_flags = {
            "dump_blotters": self.dump_blotters_var.get(),
            "dump_lobs": self.dump_lobs_var.get(),
            "dump_strats": self.dump_strats_var.get(),
            "dump_avgbals": self.dump_avgbals_var.get(),
            "dump_tape": self.dump_tape_var.get()
        }
        settings["dump_flags"] = dump_flags
        settings["output_dir"] = self.output_dir_var.get()

        return settings

    def apply_settings(self):
        """Generate a configuration file with current settings"""
        settings = self.collect_settings()

        try:
            config_path = os.path.join(os.getcwd(), "bse_config.py")
            with open(config_path, 'w') as f:
                f.write("# BSE Configuration File - Generated by BSE Settings GUI\n\n")

                # Simulation parameters
                f.write(f"n_days = {settings['n_days']}\n")
                f.write(f"hours_in_a_day = {settings['hours_in_a_day']}\n\n")

                # Trader specifications
                f.write("# Trader specifications\n")
                f.write(f"buyers_spec = {settings['buyers_spec']}\n")

                if settings.get("same_traders", True):
                    f.write("sellers_spec = buyers_spec\n")
                else:
                    f.write(f"sellers_spec = {settings['sellers_spec']}\n")

                # traders_spec = {'sellers': sellers_spec, 'buyers': buyers_spec, 'proptraders': proptraders_spec}
                f.write("proptraders_spec = []\n")
                f.write(
                    "traders_spec = {'sellers': sellers_spec, 'buyers': buyers_spec, 'proptraders': proptraders_spec}\n\n")

                # Output settings
                f.write("# Output settings\n")
                f.write(f"verbose = {str(settings['verbose'])}\n")
                f.write(f"n_trials = {settings['n_trials']}\n")
                f.write(f"n_trials_recorded = {settings['n_trials_recorded']}\n")
                f.write(f"dump_flags = {settings['dump_flags']}\n")

            messagebox.showinfo("Success", "Settings applied and saved to bse_config.py")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply settings: {str(e)}")
            return False

    def run_simulation(self):
        """Apply settings and run the BSE simulation"""
        if self.apply_settings():
            try:
                # Run the main BSE script with the config
                command = [sys.executable, "BSE.py"]
                subprocess.Popen(command)
                messagebox.showinfo("Success", "BSE simulation started")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to run simulation: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BSESettingsGUI(root)
    root.mainloop()