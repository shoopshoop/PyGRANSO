import dbg_print
from pygransoStruct import genral_struct

def makeStructWithFields(varargin):
    """
    makeStructWithFields.py
      Returns an empty struct with the fieldnames specified as input
      arguments but all set to [].
    """
    # args            = cell(1,2*nargin);
    # args(1:2:end-1) = varargin(:);
    # s               = struct(args{:});
    dbg_print("skip makeStructWithFields for now")
    s = genral_struct()
    
    return s