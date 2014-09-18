__author__ = 'prateek'

class ModelUtils(object):
    def to_dict(self):
        result = super(ModelUtils,self).to_dict()
        result['key'] = self.key.id() #get the key as a string
        return result