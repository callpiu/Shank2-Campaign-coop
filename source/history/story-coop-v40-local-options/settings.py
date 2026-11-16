"""Extend both published WinForms settings scripts without duplicating them."""


def extend(raw, lang):
    s = raw.decode('utf-8-sig').replace('\r\n', '\n')

    def edit(old, new):
        nonlocal s
        assert s.count(old) == 1, old
        s = s.replace(old, new)

    def tr(en, chs):
        return f"T '{en}' '{chs if lang == 'chs' else en}'"

    edit('$script:inputMode = 0', '$script:inputMode = 0\n$script:hudLayout = 0')
    edit('if ($mode -notin 0,1) { return }',
         'if ($mode -notin 0,1,2,4,5,6) { return }')
    edit('return @{ Keys=$values; Mode=$mode }',
         'return @{ Keys=$values; Mode=($mode -band 3); Layout=($mode -shr 2) }')
    edit('function Encode-Keys([int]$Mode,[int[]]$Values) {',
         'function Encode-Keys([int]$Mode,[int[]]$Values,[int]$Layout=0) {\n'
         "    if ($Mode -notin 0,1,2 -or $Layout -notin 0,1) { throw 'Invalid co-op settings.' }")
    edit('[BitConverter]::GetBytes($Mode).CopyTo($buffer,4)',
         '[BitConverter]::GetBytes([int]($Mode -bor ($Layout -shl 2))).CopyTo($buffer,4)')
    edit('function Save-Keys([int]$Mode,[int[]]$Values) {',
         'function Save-Keys([int]$Mode,[int[]]$Values,[int]$Layout=0) {')
    edit('Write-Atomic $keyPath (Encode-Keys $Mode $Values)',
         'Write-Atomic $keyPath (Encode-Keys $Mode $Values $Layout)')
    edit('$script:inputMode=$saved.Mode', '$script:inputMode=$saved.Mode\n        $script:hudLayout=$saved.Layout')
    edit('public int KeyCode { get; private set; }', '''public int KeyCode { get; private set; }
    public void AssignMouse(int code) {
        KeyCode = code;
        DialogResult = DialogResult.OK;
    }''')
    edit('function Key-Name([int]$Code) {', f'''function Key-Name([int]$Code) {{
    switch ($Code) {{
        1 {{ return ({tr('Left click','鼠标左键')}) }}
        2 {{ return ({tr('Right click','鼠标右键')}) }}
        4 {{ return ({tr('Middle click','鼠标中键')}) }}
    }}''')
    edit("$modeBox.DropDownStyle = 'DropDownList'", """$modeBox.DropDownStyle = 'DropDownList'
$layoutLabel = Add-Control 'Label' 363 63 65 23
$layoutBox = Add-Control 'ComboBox' 434 59 145 25
$layoutBox.DropDownStyle = 'DropDownList'""")
    edit("Add-Control 'ComboBox' 528 59 132 25", "Add-Control 'ComboBox' 587 59 73 25")
    edit('$dialog.Controls.Add($msg)', f'''$dialog.Controls.Add($msg)
        if ($Index -in 5,6,7,8,9,11,12) {{
            $dialog.ClientSize=[Drawing.Size]::new(390,111)
            $mouseLabels=@(({tr('Left click','鼠标左键')}),({tr('Right click','鼠标右键')}),({tr('Middle click','鼠标中键')}))
            for ($i=0; $i -lt 3; $i++) {{
                $mouse=[Windows.Forms.Button]::new()
                $mouse.SetBounds((18+118*$i),65,110,27)
                $mouse.Text=$mouseLabels[$i]
                $mouse.Tag=1 -shl $i
                $mouse.Add_Click({{ param($sender,$eventArgs) $sender.FindForm().AssignMouse([int]$sender.Tag) }})
                $dialog.Controls.Add($mouse)
            }}
        }}''')
    edit('$modeBox.SelectedIndex=$picked', f'''[void]$modeBox.Items.Add(({tr('1P keyboard / mouse + 2P controller','1P 键鼠 + 2P 手柄')}))
    $modeBox.SelectedIndex=$picked
    $layoutLabel.Text={tr('HUD layout','血条布局')}
    $layout=$layoutBox.SelectedIndex
    if ($layout -lt 0) {{ $layout=$script:hudLayout }}
    $layoutBox.Items.Clear()
    [void]$layoutBox.Items.Add(({tr('Side by side','左右并排')}))
    [void]$layoutBox.Items.Add(({tr('Stacked','上下排列')}))
    $layoutBox.SelectedIndex=$layout''')
    edit('for ($j=0; $j -lt 25; $j++) { $buttons[$j].Enabled=($modeBox.SelectedIndex -eq 0) }\n'
         '    for ($j=27; $j -lt 31; $j++) { $buttons[$j].Enabled=($modeBox.SelectedIndex -eq 0) }',
         '''$shared=$modeBox.SelectedIndex -eq 0
    $mixed=$modeBox.SelectedIndex -eq 2
    for ($j=0; $j -lt 25; $j++) { $buttons[$j].Enabled=($shared -or ($mixed -and $j -lt 13)) }
    for ($j=27; $j -lt 31; $j++) { $buttons[$j].Enabled=($shared -or ($mixed -and $j -lt 29)) }''')
    edit('    Update-Text\n    $status.Text=T \'Defaults restored;',
         '''    Update-Text
    $layoutBox.SelectedIndex=0
    if ($modeBox.SelectedIndex -eq 2) {
        $script:keys[5]=1
        $script:keys[7]=2
        Update-Text
    }
    $status.Text=T 'Defaults restored;''')
    edit('Save-Keys $modeBox.SelectedIndex $script:keys',
         'Save-Keys $modeBox.SelectedIndex $script:keys $layoutBox.SelectedIndex')
    edit('        $dodgeRoundTrip=Read-Dodge', '''        if ($roundTrip.Layout -ne 0) { throw 'Legacy layout default failed.' }
        $mixedKeys=$defaults.Clone()
        $mixedKeys[5]=1; $mixedKeys[7]=2
        $mixed=Read-Keys (Encode-Keys 2 $mixedKeys 1)
        if ($mixed.Mode -ne 2 -or $mixed.Layout -ne 1 -or $mixed.Keys[5] -ne 1 -or $mixed.Keys[7] -ne 2) {
            throw 'Mixed input and layout serialization failed.'
        }
        $dodgeRoundTrip=Read-Dodge''')
    edit('        foreach ($index in @(27,28,29,30))', '''        $modeBox.SelectedIndex=2
        if (!$buttons[0].Enabled -or !$buttons[27].Enabled -or $buttons[13].Enabled -or $buttons[30].Enabled -or !$buttons[26].Enabled) {
            throw 'Mixed input binding visibility failed.'
        }
        $layoutBox.SelectedIndex=1
        Update-Text
        if ($layoutBox.SelectedIndex -ne 1 -or $layoutBox.Items.Count -ne 2) { throw 'HUD layout selection failed.' }
        foreach ($index in @(27,28,29,30))''')
    return s.encode('utf-8-sig')
