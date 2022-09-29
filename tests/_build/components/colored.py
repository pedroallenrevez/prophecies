tmpl="""<p>TEST</p>
"""

from prophecies.parser import Paragraph 
from prophecies.parser import register

class colored(Paragraph):
    color: str = "blue"

register('colored', colored)