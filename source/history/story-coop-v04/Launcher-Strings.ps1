$script:uiLanguage='en'
$script:uiStrings=@{
    en=@{
        windowTitle='Shank 2 Story Co-op - v0.4 Prototype';heading='Local story co-op'
        description='Choose a character and weapons for each player. Applied when you enter a level.'
        language='Language';gameFolder='Game folder';browse='Browse...'
        chooseFolder='Select the Shank 2 folder containing bin and data-pc'
        player1='Player 1';player2='Player 2';skin='Character / outfit';melee='Melee weapon';ranged='Ranged weapon';consumable='Throwable'
        portrait='Player {0}: {1} portrait';inputMode='Input mode';keyboard='Shared keyboard';pads='Two XInput controllers'
        rescueHint='Revive a downed teammate. Retry when both are down. F6 recalls Player 2.'
        keyboardHint='Keyboard: P1 WASD / Space; P2 Arrow keys / Numpad 0 (NumLock on).'
        ready='Settings apply to this mod. The original game and earlier mods are preserved.'
        settingsUnreadable='Could not read saved settings. Default co-op loadouts are shown.'
        save='Save settings';launch='Save and launch';saved='Loadouts saved. Changes apply the next time you launch.'
        installing='Verifying files and preparing the mod...';launched='Game started. Select CAMPAIGN MODE to play the story.'
        saveErrorTitle='Could not save';launchErrorTitle='Could not launch'
        saveError='Could not save your settings.';launchError='Could not start the game.'
        launchFailed='Launch failed. Check the game folder and close any running v0.4 game.'
        languageSaveFailed='Language changed, but the preference could not be saved.'
        gameFolderRequired='Select your Shank 2 game folder using Browse.'
        removed='v0.4 mod files removed. The original game and earlier mods were preserved.'
        removeError='Could not remove the mod'
    }
    zh=@{
        windowTitle='Shank 2 故事双人 · v0.4 原型';heading='故事模式本地双人'
        description='分别选择角色和三格装备；进入关卡后采用这里保存的配装。'
        language='界面语言';gameFolder='游戏目录';browse='浏览…'
        chooseFolder='选择包含 bin 和 data-pc 的 Shank 2 游戏目录'
        player1='1P 玩家';player2='2P 玩家';skin='角色 / 服装';melee='近战装备';ranged='远程装备';consumable='投掷装备'
        portrait='{0}P {1} 头像';inputMode='输入方式';keyboard='共用键盘';pads='两个 XInput 手柄'
        rescueHint='一人倒地可由伙伴救起；双方倒地才进入重试。F6 手动召回 2P。'
        keyboardHint='键盘：1P WASD / 空格；2P 方向键 / 小键盘 0（NumLock 开启）'
        ready='设置仅供此 MOD 使用，原版程序与旧版 MOD 保留。'
        settingsUnreadable='上次配置无法读取，已使用默认双人配装。'
        save='保存配置';launch='保存并启动';saved='双人配装已保存，下次启动时生效。'
        installing='正在校验并准备 MOD…';launched='游戏已启动。选择 CAMPAIGN MODE 进入故事模式。'
        saveErrorTitle='无法保存';launchErrorTitle='启动失败'
        saveError='无法保存设置。';launchError='无法启动游戏。'
        launchFailed='未能启动，请检查游戏目录并关闭已运行的 v0.4。'
        languageSaveFailed='界面语言已切换，但未能保存语言偏好。'
        gameFolderRequired='请点击“浏览”选择你电脑上的 Shank 2 游戏目录。'
        removed='v0.4 MOD 文件已移除，原版游戏与旧版 MOD 已保留。'
        removeError='无法移除 MOD'
    }
}
$script:weaponNamesZh=@{
    machete='砍刀';saw='电锯';sledgehammer='大锤';throwingknives='飞刀';pistols='双枪';shotgun='霰弹枪'
    sword='长剑';scythe='镰刀';revolver='左轮手枪';uzi='乌兹冲锋枪'
    weapon_grenade='手雷';weapon_mine='地雷';weapon_molotov='燃烧瓶'
}
$script:skinNamesZh=@{
    shank='Shank（默认）';falcone='Falcone';classic='Classic（经典）';defender='Defender（守护者）'
    explorer='Junior（少年）';hobo='Hobo（流浪汉）';luchador='Rex（摔角手）';yakuza='Rin（极道）'
    boogie='Boogie';horror='Horror（恐怖）';cesar='Cesar';evil='Evil（邪恶）'
    corina='Corina（默认）';bubbles='Bubbles';superheroine='Kats（女英雄）';track='Chops（运动员）';sunshine='Sunshine'
}
function Get-UiText([string]$Key) {
    $value=$script:uiStrings[$script:uiLanguage][$Key]
    if($null -eq $value) {throw ('Missing UI translation: '+$script:uiLanguage+'/'+$Key)}
    return [string]$value
}
function Get-SkinItem($Skin) {
    $name=$Skin.name
    if($script:uiLanguage -eq 'zh' -and $script:skinNamesZh.ContainsKey($Skin.id)) {$name=$script:skinNamesZh[$Skin.id]}
    return [pscustomobject]@{id=$Skin.id;name=$name;family=$Skin.family;hash=$Skin.hash}
}
function Get-WeaponName($Weapon) {
    if($script:uiLanguage -eq 'zh' -and $script:weaponNamesZh.ContainsKey($Weapon.id)) {return $script:weaponNamesZh[$Weapon.id]}
    return [string]$Weapon.name
}
