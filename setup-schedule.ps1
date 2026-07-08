# 本草堂 · Windows 定时任务设置
# 每天自动生成内容
# 右键 → 以管理员身份运行 PowerShell → 执行此脚本

$action = New-ScheduledTaskAction -Execute "C:\Users\Admin\agent-workstation\.venv\Scripts\python.exe" -Argument "C:\Users\Admin\agent-workstation\bots\auto_pilot.py --mode today" -WorkingDirectory "C:\Users\Admin\agent-workstation"
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00AM
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "本草堂每日内容生成" -Action $action -Trigger $trigger -Settings $settings -Description "每天自动生成本草堂全平台营销内容" -User $env:USERNAME
Write-Output "✅ 定时任务已设置：每天早上 6:00 自动生成当日内容"
