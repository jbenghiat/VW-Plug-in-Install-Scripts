import vs

kSDKTool = 1
kVectorScriptTool = 2
kVectorScriptObject = 3
kSDKParametric = 4

def GetPalettePath(paletteName):
    totalPalettes = vs.ws2GetToolsCnt("")
    curPalette = 0
    outPath = ""
    while curPalette < totalPalettes:
        pName = vs.ws2GetToolAt("", curPalette)
        result, outDisplayName, outShortcutKey, outShortcutKeyModifier, outResourceID = vs.ws2GetToolInfo(
            pName)
        if (outDisplayName == paletteName):
            outPath = pName
            break
        curPalette = curPalette + 1

    return outPath


def GetToolsetPath(paletteName, tsName):
    outPath = ""
    palletteUName = GetPalettePath(paletteName)
    if (palletteUName != ""):
        totalToolSets = vs.ws2GetToolsCnt(palletteUName)
        curToolSet = 0
        tsUName = ""
        while curToolSet < totalToolSets:
            tsUName = vs.ws2GetToolAt(palletteUName, curToolSet)
            result, outDisplayName, outShortcutKey, outShortcutKeyModifier, outResourceID = vs.ws2GetToolInfo(
                palletteUName + "/" + tsUName)
            if (outDisplayName == tsName):
                outPath = palletteUName + "/" + tsUName
                break
            curToolSet = curToolSet + 1
    return outPath


def GetMenuPathByName(menuName, rootpath = ""):
    totalMenus = vs.ws2GetMenusCnt(rootpath)
    curMenu = 0
    outPath = ""
    while curMenu < totalMenus:
        mName = vs.ws2GetMenuAt(rootpath, curMenu)
        if rootpath != "":
            mName = "/".join([rootpath, mName])
        outDisplayName, outHasShortcut, outShortcutKey, outShortcutKeyModifier = vs.ws2GetMenuInfo(
            mName)
        if (outDisplayName == menuName):
            outPath = mName
            break
        curMenu = curMenu + 1
    return outPath

#
#   Pick Palette Dialog
#


def PickPalette():
    global palettePath

    # control IDs
    kOK = 1
    kCancel = 2
    kListPalette = 4

    def CreateDialog():
        # Alignment constants
        kRight = 1
        kBottom = 2
        kLeft = 3
        kColumn = 4
        kResize = 0
        kShift = 1

        def GetPluginString(ndx):
            # Static Text
            if ndx == 1001:
                return 'Add'
            elif ndx == 1002:
                return 'Cancel'
            elif ndx == 1003:
                return 'Select Tool Palette'
            elif ndx == 1004:
                return ''
            # Help Text
            elif ndx == 2001:
                return 'Add installed plug-ins to the selected tool palette.'
            elif ndx == 2002:
                return 'Do not add. You can still manually edit your workspace to add the plug-in.'
            elif ndx == 2004:
                return 'Select a palette to which to add the plug-ins.'
            return ''

        def GetStr(ndx):
            result = GetPluginString(ndx + 1000)
            return result

        def GetHelpStr(ndx):
            result = GetPluginString(ndx + 2000)
            return result

        dialog = vs.CreateResizableLayout(
            GetStr(3), True, GetStr(kOK), GetStr(kCancel), True, True)

        # create controls
        vs.CreateListBox(dialog, kListPalette, 30, 15)

        # set relations
        vs.SetFirstLayoutItem(dialog, kListPalette)

        # set bindings
        vs.SetEdgeBinding(dialog, kListPalette, True, True, True, True)

        # set help strings
        cnt = 1
        while (cnt <= 4):
            vs.SetHelpText(dialog, cnt, GetHelpStr(cnt))
            cnt += 1

        return dialog

    palettes = {}

    # Dialog handler
    def DialogHandler(item, data):
        if item == 12255:  # SetupDialogC
            totalPalettes = vs.ws2GetToolsCnt("")
            curPalette = 0
            while curPalette < totalPalettes:
                pName = vs.ws2GetToolAt("", curPalette)
                result, outPDisplayName, outShortcutKey, outShortcutKeyModifier, outResourceID = vs.ws2GetToolInfo(
                    pName)
                totalTS = vs.ws2GetToolsCnt(pName)
                curTS = 0
                while curTS < totalTS:
                    tsName = vs.ws2GetToolAt(pName, curTS)
                    result, outTDisplayName, outShortcutKey, outShortcutKeyModifier, outResourceID = vs.ws2GetToolInfo(
                        pName + "/" + tsName)
                    palettes[outPDisplayName + '>' +
                             outTDisplayName] = pName + "/" + tsName
                    curTS += 1
                curPalette += 1
            idx = 0
            for displayName in palettes:
                vs.AddChoice(dlg_select_palette,
                             kListPalette, displayName, idx)
                idx += 1
        elif item == kOK:
            idx, displayName = vs.GetSelectedChoiceInfo(
                dlg_select_palette, kListPalette, 0)
            global palettePath
            palettePath = palettes[displayName]

        idx, displayName = vs.GetSelectedChoiceInfo(
            dlg_select_palette, kListPalette, 0)
        vs.EnableItem(dlg_select_palette, kOK, idx > -1)

    dlg_select_palette = CreateDialog()
    ok = (vs.RunLayoutDialog(dlg_select_palette, DialogHandler) == kOK)

    return (ok, palettePath)


def PromptAddToWorkspace(productName, ModifyWorkspace, major):
    if major < 26:
        vs.AlrtDialog(productName + " Installation Complete.")
    else:
        # Add to workspace
        if vs.AlertQuestion(productName + ' Installation Complete', 'Add to the current workspace (Not needed for existing installations)?', 1, 'Yes', 'No', '', ''):
            try:
                ModifyWorkspace()

                restart = False
                reload = True
                vs.ws2CommitChanges(restart, reload)
            except:
                vs.AlrtDialog("Workspace modification failed")
