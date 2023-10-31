# import ...

class HighlightedText:
    """Class that defines a text in which certain words will be highlighted with certain colours"""

    def __init__(self,text,range_values=(-1,1),colour_list=None):

        self.text = text
        self.tokens_list = self.text.split(' ')

        self.values_dict = {token:None for token in self.tokens_list}

        self.range_values = range_values
        self.min_value = self.range_values[0]
        self.max_value = self.range_values[1]

        if colour_list is None:
            # default colour list
            colour_list = gren2blue
        self.palette = Palette(colour_list)

    def set_values(self,func):
        """It takes a function that takes tokens and returns a float. Assigns the values for highlighting"""
        for token in self.tokens_list:
            self.values_dict[token] = func(token)
        
    def colour_token(self,token):
        value = self.values_dict[token]
        scaled_value =  (value -self.min_value) / (self.max_value - self.min_value)
        return self.palette(scaled_value)
    
    def text_html(self):
        coloured_tokens = []
        for token in self.tokens_list:
            if self.values_dict[token] is not None:
                new_str = """<span style="color: {};">{}</span>""".format(self.colour_token(token),token)
                coloured_tokens.append(new_str)
            else:
                coloured_tokens.append(token)
        return ' '.join(coloured_tokens)
    
    def render(self,filename='visualisation.html'):
        html = """<!DOCTYPE html>\n<html>\n<head>\n\t<style>\n\t\t.centered-text {text-align: center;}\n\t\t.large-text { font-size: 24px; }
        \t</style>\n</head>\n<body>\n\t<div class="centered-text">\n\t\t<p class="large-text">REPLACE_WITH_TEXT</p>\n\t</div>\n</body>\n</html>"""
        html = html.replace('REPLACE_WITH_TEXT',self.text_html())
        with open(filename, 'w') as file:
            file.write(html)
        return html
        

class Palette:
    def __init__(self,colour_list):
        """Initalises class Palette with a colour list that has an order"""
        self._colour_list = colour_list
    
    def __len__(self):
        return len(self._colour_list)
    
    def get_partition_index(self, x):
        n = self.__len__()

        if x < -1 or x > 1:
            return "Number is out of range [-1, 1]"
        
        segment_size = 2 / n  # Calculate the size of each segment
        partition = [-1 + i * segment_size for i in range(n + 1)]
        
        for i in range(n):
            if x >= partition[i] and x <= partition[i + 1]:
                return i  # Return the index of the segment
        
        return n  # If x == 1, it belongs to the last segment
    
    def __call__(self,x):
        n = self.get_partition_index(x)
        return self._colour_list[n]


# Some example colour lists

gren2blue = [
    "#00D40E",  # green
    "#00BA2D",
    "#009658",
    "#007185",
    "#0053A8",
    "#003193",  # blue
]
