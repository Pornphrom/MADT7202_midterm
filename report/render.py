from pathlib import Path
import sys
from render_update4 import render
if __name__ == '__main__':
    render(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent/'MADT7202_MidTerm_Palaloy_Revised.pdf')
