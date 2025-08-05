from obswebsocket import obsws, requests

class OBSWebsocketsManager:
    def __init__(self, host, port, password):
        """Initialize and connect to OBS WebSocket."""
        self.obs = obsws(host, port, password)
        self.obs.connect()

    def disconnect(self):
        """Disconnect from OBS WebSocket."""
        self.obs.disconnect()

    def set_scene(self, new_scene):
        """Set the current scene in OBS."""
        self.obs.call(requests.SetCurrentProgramScene(sceneName=new_scene))

    def set_filter_visibility(self, source_name, filter_name, filter_enabled=True):
        """Set the visibility of a filter on a source."""
        self.obs.call(requests.SetSourceFilterEnabled(
            sourceName=source_name,
            filterName=filter_name,
            filterEnabled=filter_enabled
        ))

    def set_source_visibility(self, scene_name, source_name, source_visible=True):
        """Set the visibility of a source in a specific scene."""
        resp = self.obs.call(requests.GetSceneItemId(
            sceneName=scene_name,
            sourceName=source_name
        ))
        item_id = resp.datain['sceneItemId']
        self.obs.call(requests.SetSceneItemEnabled(
            sceneName=scene_name,
            sceneItemId=item_id,
            sceneItemEnabled=source_visible
        ))

    def get_text(self, source_name):
        """Get the text of a text source."""
        resp = self.obs.call(requests.GetInputSettings(inputName=source_name))
        return resp.datain['inputSettings']['text']

    def set_text(self, source_name, new_text):
        """Set the text of a text source."""
        self.obs.call(requests.SetInputSettings(
            inputName=source_name,
            inputSettings={'text': new_text}
        ))

    def get_source_transform(self, scene_name, source_name):
        """Get the transform of a source in a scene."""
        resp = self.obs.call(requests.GetSceneItemId(
            sceneName=scene_name,
            sourceName=source_name
        ))
        item_id = resp.datain['sceneItemId']
        resp = self.obs.call(requests.GetSceneItemTransform(
            sceneName=scene_name,
            sceneItemId=item_id
        ))
        t = resp.datain['sceneItemTransform']
        return {
            'positionX': t['positionX'],
            'positionY': t['positionY'],
            'scaleX': t['scaleX'],
            'scaleY': t['scaleY'],
            'rotation': t['rotation'],
            'sourceWidth': t['sourceWidth'],
            'sourceHeight': t['sourceHeight'],
            'width': t['width'],
            'height': t['height'],
            'cropLeft': t['cropLeft'],
            'cropRight': t['cropRight'],
            'cropTop': t['cropTop'],
            'cropBottom': t['cropBottom'],
        }

    def set_source_transform(self, scene_name, source_name, new_transform):
        """Set the transform of a source in a scene."""
        resp = self.obs.call(requests.GetSceneItemId(
            sceneName=scene_name,
            sourceName=source_name
        ))
        item_id = resp.datain['sceneItemId']
        self.obs.call(requests.SetSceneItemTransform(
            sceneName=scene_name,
            sceneItemId=item_id,
            sceneItemTransform=new_transform
        ))

    def get_input_settings(self, input_name):
        """Get settings for a specific input."""
        return self.obs.call(requests.GetInputSettings(inputName=input_name))

    def get_input_kind_list(self):
        """Get a list of all input kinds available in OBS."""
        return self.obs.call(requests.GetInputKindList())

    def get_scene_items(self, scene_name):
        """Get a list of all items in a specific scene."""
        return self.obs.call(requests.GetSceneItemList(sceneName=scene_name))