Python scripts to aid in the installation of Vectorworks plug-ins using the install manager or partner products install process.

Include in the install package, and include relative to install.py

Example usage:
```python
# Adds a tool along side an existing tool if found, or a user-selected tool set if not

# import the helper module
# the try/except allows looking in the install package first, then in your python paths so that you can run from the Run Script... menu
try:
    from . import workspace_edit as we
except:
    import workspace_edit as we

#
# Modify this function to build the workspace for each install package
#
def ModifyWorkspace():
    # Try to find the tool set containing an existing tool
    tsMyPlugin = we.GetToolsetPath('Tool Sets', 'ExistingPlugin')

    # If found, set the install path for MyPluginTool to the tool set
    if (tsMyPlugin != ''):
        addPath = tsMyPlugin
        ok = True
    # Otherwise, ask user so select an existing tool set
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
