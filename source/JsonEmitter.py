import json

class JsonEmitter:
    def __init__(self, indent=4):
        self.indent = indent

    def emit(self, keypoints, angles, timestamp):
        """
        Restituisce il JSON con i 3 campi dati in input, null se non trovati
        """

        json_obj = {
            "timestamp": timestamp,
            "keypoints": keypoints,
            "angles": angles
        }
        
        return json.dumps(json_obj, indent=self.indent)