# Installer matrix for the on-by-default hook. Runs the real install.ps1 / uninstall.ps1 against throwaway
# home folders and checks every case a machine can be in. Run it with BOTH Windows PowerShell and PowerShell 7:
#   powershell -NoProfile -ExecutionPolicy Bypass -File tests\install-matrix.ps1
#   pwsh -NoProfile -File tests\install-matrix.ps1
# Exit code 0 = every check passed. Never touches the real ~\.claude.
$ErrorActionPreference = "Stop"
$Repo = Split-Path -Parent $PSScriptRoot
$Ver = "$($PSVersionTable.PSVersion.Major).$($PSVersionTable.PSVersion.Minor)"
$Root = Join-Path ([IO.Path]::GetTempPath()) "a-install-matrix-$PID"
$Fail = 0
function Check([string]$Name, [bool]$Ok) { if ($Ok) { Write-Host "ok   $Name" } else { Write-Host "FAIL $Name"; $script:Fail++ } }
function Read-Utf8([string]$Path) { [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8) }
function Write-Utf8([string]$Path, [string]$Text) { [IO.File]::WriteAllText($Path, $Text, (New-Object Text.UTF8Encoding $false)) }
function Get-OurHooks($s) { @(@($s.hooks.UserPromptSubmit) | ForEach-Object { @($_.hooks) } | Where-Object { $_ -and "$($_.command)" -like "*auto-pointer.md*" }) }
function Invoke-Hook($h) {   # run the hook the way Claude Code does: the named shell, the command as written
  # "powershell" may mean Windows PowerShell or PowerShell 7 depending on the host, so every one present must pass.
  $exes = if ($h.shell -eq "powershell") { @("powershell", "pwsh") | Where-Object { Get-Command $_ -ErrorAction SilentlyContinue } } else { @("bash") }
  foreach ($exe in $exes) {
    if ($exe -eq "bash") { $out = & bash -c $h.command 2>&1 } else { $out = & $exe -NoProfile -Command $h.command 2>&1 }
    @{ Exe = $exe; Out = ($out | Out-String); Code = $LASTEXITCODE }
  }
}
$Unicode = "caf$([char]0xE9) $([char]0x65E5)$([char]0x672C) $([char]0x2014)"   # e-acute, two CJK characters, an em dash: must survive install and uninstall
$Cases = [ordered]@{
  "missing settings.json" = $null
  "empty settings.json"   = ""
  "settings with other hook, token, non-English text" = "{`"env`":{`"FAKE_TOKEN`":`"keep-me`",`"NOTE`":`"$Unicode`"},`"hooks`":{`"UserPromptSubmit`":[{`"hooks`":[{`"type`":`"command`",`"command`":`"echo other`"}]}]}}"
  "settings that is not plain JSON" = "// a comment`n{`"env`":{}}"
}
Write-Host "install-matrix on PowerShell $Ver ($($PSVersionTable.PSEdition))"
$OldProfile = $env:USERPROFILE
try {
  foreach ($case in $Cases.Keys) {
    $H = Join-Path $Root ($case -replace '[^a-z]', '')
    New-Item -ItemType Directory -Force (Join-Path $H ".claude") | Out-Null
    $SetPath = Join-Path $H ".claude\settings.json"
    if ($null -ne $Cases[$case]) { Write-Utf8 $SetPath $Cases[$case] }
    $before = if (Test-Path $SetPath) { Read-Utf8 $SetPath } else { $null }
    $env:USERPROFILE = $H
    $log = (& "$Repo\install.ps1" *>&1 | Out-String) + (& "$Repo\install.ps1" *>&1 | Out-String)   # twice: must not duplicate
    $env:USERPROFILE = $OldProfile
    $pointer = Join-Path $H ".a\auto-pointer.md"
    Check "[$case] pointer is plain ASCII" (-not ((Read-Utf8 $pointer) -match '[^\x00-\x7F]'))
    if ($case -like "*not plain JSON*") {
      Check "[$case] settings left byte-for-byte untouched" ((Read-Utf8 $SetPath) -eq $before)
      Check "[$case] installer says NOT added" ($log -match "NOT added")
      continue
    }
    $obj = (Read-Utf8 $SetPath) | ConvertFrom-Json
    $ours = @(Get-OurHooks $obj)
    Check "[$case] exactly one A Skill hook after two installs" ($ours.Count -eq 1)
    Check "[$case] hook names its shell" ($ours[0].shell -eq "powershell")
    $r = Invoke-Hook $ours[0]
    Check "[$case] hook prints the pointer, exit 0" (($r.Out -match "^The A Skill is the default workflow") -and $r.Code -eq 0)
    Check "[$case] hook output is plain ASCII" (-not ($r.Out -match '[^\x00-\x7F]'))
    if ($case -like "*other hook*") {
      Check "[$case] other hook kept" (@(@($obj.hooks.UserPromptSubmit) | ForEach-Object { @($_.hooks) } | Where-Object { $_.command -eq "echo other" }).Count -eq 1)
      Check "[$case] token kept" ($obj.env.FAKE_TOKEN -eq "keep-me")
      Check "[$case] non-English text intact" ($obj.env.NOTE -eq $Unicode)
    }
    Rename-Item $pointer "auto-pointer.md.hidden"
    foreach ($r in Invoke-Hook $ours[0]) { Check "[$case] pointer missing: hook in $($r.Exe) says so, exit 0" (($r.Out -match "pointer file missing") -and $r.Code -eq 0) }
    Rename-Item "$pointer.hidden" "auto-pointer.md"
    $env:USERPROFILE = $H
    & "$H\.a\templates\uninstall.ps1" -Yes *>&1 | Out-Null
    $env:USERPROFILE = $OldProfile
    $obj = (Read-Utf8 $SetPath) | ConvertFrom-Json
    Check "[$case] uninstall removes the hook" (@(Get-OurHooks $obj).Count -eq 0)
    Check "[$case] uninstall removes pointer and Copilot file" (-not (Test-Path $pointer) -and -not (Test-Path (Join-Path $H ".copilot\instructions\a-skill.instructions.md")))
    if ($case -like "*other hook*") { Check "[$case] after uninstall: other hook, token, non-English text intact" (($obj.env.NOTE -eq $Unicode) -and ($obj.env.FAKE_TOKEN -eq "keep-me") -and (@($obj.hooks.UserPromptSubmit).Count -eq 1)) }
  }
} finally { $env:USERPROFILE = $OldProfile; Remove-Item -Recurse -Force $Root -ErrorAction SilentlyContinue }
Write-Host $(if ($Fail) { "$Fail check(s) FAILED on PowerShell $Ver" } else { "all checks passed on PowerShell $Ver" })
exit $Fail
