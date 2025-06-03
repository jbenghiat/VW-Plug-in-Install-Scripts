Python scripts to aid in the installation of Vectorworks plug-ins using the install manager or partner products install process.

Include in the install package, and include relative to install.py

Example usage:
```python
try:
    from . import workspace_edit as we
except:
    import workspace_edit as we

#
# Modify this function to build the workspace for each install package
#
def ModifyWorkspace():
    # Check if MyPlugin TS exists
    tsMyPlugin = we.GetToolsetPath('Tool Sets', 'MyPlugin')

    # If so, add to TS
    if (tsMyPlugin != ''):
        addPath = tsMyPlugin
        ok = True
    # Otherwise, ask user for TS
    else:
        ok, addPath = we.PickPalette()
    if ok:
        vs.ws2CreateTool(addPath, "MyPluginTool", we.kSDKTool)

if __name__ == "__main__":
    ModifyWorkspace()
    restart = False
    reload = True
    vs.ws2CommitChanges(restart, reload)
    vs.AlrtDialog("Workspace modified")

```
