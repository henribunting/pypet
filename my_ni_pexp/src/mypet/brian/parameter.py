'''
Created on 10.06.2013

@author: robert
'''


from mypet.parameter import Parameter
from brian.units import *
from brian.stdunits import *
from brian.fundamentalunits import Unit


class BrianParameter(Parameter):
    ''' The standard Brian Parameter that has a value and a unit
    
    The unit has to be set via param.unit = unit,
    e.g.
    >>> param.unit = mV
    
    the corresponding value is set as
    >>> param.value = 10
    
    If both have been specified
    a call to the param returns the corresponding brian quantity:
    >>> print param()
    >>> 10*mvolt
    
    The brian quantity can also be accessed via param.val
    
    '''

    def __call__(self,valuename=None):
        if not valuename or valuename == 'val':
            unit = eval(self.unit)
            value = self.value
            return value*unit   
        else:
            super(BrianParameter,self).__call__(valuename)
            
    def __getattr__(self,name):
        if not hasattr(self, '_data'):
            raise AttributeError('This is to avoid pickling issues!')
        
        if name == 'val':
            return self()
        
        return self.get(name)
    
    def _set_single(self,name,val):
        
        ## Check if unit exists
        if name == 'unit':
            unit = eval(val)
            if not isinstance(unit, Unit):
                raise ValueError('Not a unit!')
        
        super(BrianParameter,self)._set_single(name,val)

    