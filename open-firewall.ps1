# 本草堂 · 开放外网访问
# 右键 → 以管理员身份运行 PowerShell → 执行此脚本

Write-Output "正在开放 8501 端口..."
New-NetFirewallRule -DisplayName "本草堂网站" -Direction Inbound -Protocol TCP -LocalPort 8501 -Action Allow -Profile Any 2>$null
Write-Output "✅ 防火墙已开放"
Write-Output ""
Write-Output "你的外网访问地址:"
$ip = (Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing).Content
Write-Output "http://${ip}:8501"
Write-Output ""
Write-Output "把这个地址发给任何人，他们就能打开本草堂！"
Write-Output ""
Write-Output "⚠️ 如果还是访问不了，可能是路由器没有端口转发。"
Write-Output "   需要在路由器后台设置「端口映射」：外部8501 → 内部172.20.21.34:8501"
pause
