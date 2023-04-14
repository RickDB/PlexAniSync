param(
    [Parameter(Position = 0, ValueFromRemainingArguments)]
    $Args
)

# these are set from Tautulli and cause a crash if not unset
Remove-Item Env:PYTHONPATH, Env:PYTHONHOME 2>&1 | Out-Null

python TautulliSyncHelper.py $Args