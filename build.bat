pyinstaller --onefile CS7000_convert_gui.py ^
  --splash CS7000_splash_scaled.png ^
  --add-data "K3JSJ_avatar_256_by_256.png;." ^
  -n CS7000_convert_gui-v1.3.2-beta
