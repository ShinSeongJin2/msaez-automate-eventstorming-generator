# 로컬에서 main.py를 새로운 윈도우로 실행
# bash .\commands\local\runs\run_main_dev.sh

window_title="MSAEZAutomateEventStormingGenerator"
window_command="uv run python ./src/eventstorming_generator/main.py"

powershell -Command "Start-Process powershell -ArgumentList '-NoExit -Command \"\$host.UI.RawUI.WindowTitle = ''$window_title''; $window_command\"'"