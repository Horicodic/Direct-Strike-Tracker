# Direct-Strike-Tracker
A tracker for the WC3 custom game Direct Strike

# Bash Build command
python -m PyInstaller --clean --onefile --noconsole --icon=icons/logo.ico --add-data "UnitPortraits;UnitPortraits" --add-data "icons;icons" --name DST main.py