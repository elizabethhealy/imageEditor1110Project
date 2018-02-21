"""
The primary controller module for the Imager application

This module provides all of the image processing operations that are called
whenever you press a button. Some of these are provided for you and others you
are expected to write on your own.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Elizabeth Healy (eah255)
Date:    November 15, 2017 (Python 3 Version)
"""
import a6history
import math


class Editor(a6history.ImageHistory):
    """
    A class that contains a collection of image processing methods
    
    This class is a subclass of ImageHistory.  That means it inherits all of the
    methods and attributes of that class.  We do that (1) to put all of the image
    processing methods in one easy-to-read place and (2) because we might want to
    change how we 
    implement the undo functionality later.
    
    This class is broken up into three parts (1) implemented non-hidden methods,
    (2) non-implemented non-hidden methods and (3) hidden methods.  The non-hidden
    methods each correspond to a button press in the main application.  The
    hidden methods are all helper functions.
    
    Each one of the non-hidden functions should edit the most recent image in the
    edit history (which is inherited from ImageHistory).
    """
    
    # PROVIDED ACTIONS (STUDY THESE)
    def invert(self):
        """
        Inverts the current image, replacing each element with its color
        complement
        """
        current = self.getCurrent()
        for pos in range(current.getLength()):
            rgb = current.getFlatPixel(pos)
            red   = 255 - rgb[0]
            green = 255 - rgb[1]
            blue  = 255 - rgb[2]
            rgb = (red,green,blue) # New pixel value
            current.setFlatPixel(pos,rgb)
    
    
    def transpose(self):
        """
        Transposes the current image
        
        Transposing is tricky, as it is hard to remember which values have been
        changed and which have not.  To simplify the process, we copy the current
        image and usethat as a reference.  So we change the current image with
        setPixel, but read
        (with getPixel) from the copy.
        
        The transposed image will be drawn on the screen immediately afterwards.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(col,row))
    
    
    def reflectHori(self):
        """
        Reflects the current image around the horizontal middle.
        """
        current = self.getCurrent()
        for h in range(current.getWidth()//2):
            for row in range(current.getHeight()):
                k = current.getWidth()-1-h
                current.swapPixels(row,h,row,k)
    
    
    def rotateRight(self):
        """
        Rotates the current image left by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a vertical
        reflection. However, this is slow, so we use the faster strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(
                    original.getHeight()-col-1,row))
    
    
    def rotateLeft(self):
        """
        Rotates the current image left by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a vertical
        reflection. However, this is slow, so we use the faster strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        #print(current.getHeight())
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(
                    col,original.getWidth()-row-1))
    
    
    # ASSIGNMENT METHODS (IMPLEMENT THESE)
    def reflectVert(self):
        """ 
        Reflects the current image around the vertical middle.
        """
        current = self.getCurrent()
        """ for h in range(current.getWidth()//2):
            for row in range(current.getHeight()):
                k = current.getWidth()-1-h
                current.swapPixels(row,h,row,k)"""
        for h in range(current.getHeight()//2):
            for col in range(current.getWidth()):
                k=current.getHeight()-1-h
                current.swapPixels(h,col,k,col)
    
    
    def monochromify(self, sepia):
        """
        Converts the current image to monochrome, using either greyscale or
        sepia tone.
        
        If `sepia` is False, then this function uses greyscale.  It removes all
        color from the image by setting the three color components of each pixel
        to that pixel's 
        overall brightness, defined as 
            
            0.3 * red + 0.6 * green + 0.1 * blue.
        
        If sepia is True, it makes the same computations as before but sets green
        to 0.6 * brightness and blue to 0.4 * brightness.
        
        Parameter sepia: Whether to use sepia tone instead of greyscale.
        Precondition: sepia is a bool
        """
        assert isinstance(sepia,bool), repr(sepia)+' is not a bool'
        current=self.getCurrent()
        if (sepia==False):
            for pos in range(current.getLength()):
                rgb = current.getFlatPixel(pos)
                brightness=0.3*rgb[0]+0.6*rgb[1]+0.1*rgb[2]
                rgb = (int(round(brightness)), int(round(brightness)),
                       int(round(brightness)))
                current.setFlatPixel(pos,rgb)
        else:
            for pos in range(current.getLength()):
                rgb = current.getFlatPixel(pos)
                brightness=0.3*rgb[0]+0.6*rgb[1]+0.1*rgb[2]
                red=brightness
                green = brightness*0.6
                blue  = brightness*0.4
                rgb = (int(round(red)),int(round(green)),
                       int(round(blue))) # New pixel value
                current.setFlatPixel(pos,rgb)
    
    
    def jail(self):
        """
        Puts jail bars on the current image
        
        The jail should be built as follows:
        * Put 3-pixel-wide horizontal bars across top and bottom,
        * Put 4-pixel vertical bars down left and right, and
        * Put n 4-pixel vertical bars inside, where n is (number of columns - 8)
        // 50.
        
        The n+2 vertical bars should be as evenly spaced as possible.
        """
        current=self.getCurrent()
        pix=(255,0,0)
        self._drawHBar(0,pix)
        self._drawHBar(current.getHeight()-3,pix)
        ncol=current.getWidth()
        n=(ncol-8)//50
        self._drawVBar(0,pix)
        self._drawVBar(current.getWidth()-4,pix)
        actw=current.getWidth()-8
        totspace=actw-n*4
        spacebtw=totspace/(n+1)
        #print (spacebtw)
        for x in range(n):
            self._drawVBar(int(round((x+1)*(4+spacebtw))),pix)
            
                
    def vignette(self):
        """
        Modifies the current image to simulates vignetting (corner darkening).
        
        Vignetting is a characteristic of antique lenses. This plus sepia tone
        helps give a photo an antique feel.
        
        To vignette, darken each pixel in the image by the factor
        
            1 - (d / hfD)^2
        
        where d is the distance from the pixel to the center of the image and hfD 
        (for half diagonal) is the distance from the center of the image to any of 
        the corners.
        """
        current=self.getCurrent()
        xc=int(round(current.getWidth())/2)
        yc=int(round(current.getHeight())/2)
        hfD=self._distance(xc,yc,0,0)
        #print(str(hfD)+'is hfd')
        for x in range(current.getWidth()):
            for y in range(current.getHeight()):
                rgb=current.getPixel(y,x)
                d=self._distance(xc,yc,x,y)
                j=d/hfD
                #print (str(j)+'is j')
                darken= 1-j*j
                if (darken<0):
                    darken=darken*-1
                red=rgb[0]*darken
                green=rgb[1]*darken
                blue=rgb[2]*darken
                rgb = (int(round(red)), int(round(green)), int(round(blue)))
                current.setPixel(y,x,rgb)
    
    
    def pixellate(self,step):
        """
        Pixellates the current image to give it a blocky feel.
        
        To pixellate an image, start with the top left corner (e.g. the first row
        and column).  Average the colors of the step x step block to the right and
        down from this corner (if there are less than step rows or step columns,
        go to the edge of the image). Then assign that average to ALL of the
        pixels in that block.
        
        When you are done, skip over step rows and step columns to go to the next 
        corner pixel.  Repeat this process again.  The result will be a pixellated
        image.
        
        Parameter step: The number of pixels in a pixellated block
        Precondition: step is an int > 0
        """
        current=self.getCurrent()
        assert isinstance(step,int) and 0<step<current.getHeight()
        assert step<current.getWidth()
        
        for row in range(current.getHeight()):
            if(row%step==0):
                for col in range(current.getWidth()):
                    if(col%step==0):
                        avg=self._averageStep(row,col,step)
                        self._setPixAvg(row,col,step,avg)
                        

    def encode(self, text):
        """
        Returns: True if it could hide the given text in the current image; False
        otherwise.
        
        This method attemps to hide the given message text in the current image.
        It uses the ASCII representation of the text's characters.
        If successful, it returns
        True.
        
        If the text has more than 999999 characters or the picture does not have
        enough pixels to store the text, this method returns False without storing
        the message.
        
        Parameter text: a message to hide
        Precondition: text is a string
        """
        assert isinstance(text,str), repr(text)+'is not a string'
        current=self.getCurrent()
        key='&&&==='
        lennum=len(str(len(text)))
        length=len(current.getPixels())-math.ceil(lennum/3)-len(key)
        if(len(text)>999999 or len(text)>length):
            #print('false')
            return False
        
        #put in the length of the text in beginning pixels
        lentext=len(text)
        pixelpos=0
        for x in range(math.ceil(lennum/3)):
            c=lentext%1000
            self._encode_pixel(pixelpos,c)
            lentext=lentext//1000
            pixelpos=pixelpos+1
            #print('length encoded at '+str(pixelpos-1))
        
        #put in key
        for x in range(len(key)):
            self._encode_pixel(pixelpos,key[x])
            pixelpos=pixelpos+1
        
        #encode text
        for x in range(len(text)):
            c=text[x]
            self._encode_pixel(pixelpos,c)
            pixelpos=pixelpos+1
        #print('it worked')
        #string=''
        #print(len(text))
        #print(current.getPixels()[math.ceil(lennum/3)-1])
        #print(current.getPixels()[math.ceil(lennum/3):math.ceil(lennum/3)+3])
        #totallen=len(key)+math.ceil(lennum/3)+len(text)
        #print (self._decode_pixel(1))
        return True

    
    def decode(self):
        """
        Returns: The secret message stored in the current image. 
        
        If no message is detected, it returns None
        """
        key='&&&==='
        # when deoding text length - the last part of the length
        # is in the first pixel and so on... so 9800 - first pixel: 800, second
        #pixel:009
        # so first pixel*10^(3^n)+second pixel*10^(3^n) where n is the pixelpos
        current=self.getCurrent()
        string=''
        for x in range(len(current.getPixels())):
            num=self._decode_pixel(x)
            string=string+chr(num)
        if string.find(key)==-1:
            return None
        posAnd=string.find(key)
        #print('pos and:'+str(posAnd))
        length=0
        for x in range(posAnd):
            #print('x'+repr(x))
            length=length+self._decode_pixel(x)*10**(3*x)
        #print('length:'+repr(length))
        posStart=posAnd+len(key)
        mesage=string[posStart:posStart+length]
        return mesage
    
    
    # HELPER FUNCTIONS
    def _drawHBar(self, row, pixel):
        """
        Draws a horizontal bar on the current image at the given row.
        
        This method draws a horizontal 3-pixel-wide bar at the given row of the
        current image. This means that the bar includes the pixels row, row+1,
        and row+2. The bar uses the color given by the pixel value.
        
        Parameter row: The start of the row to draw the bar
        Precondition: row is an int, with 0 <= row  &&  row+2 < image height
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is
        0..255
        """
        current = self.getCurrent()
        assert isinstance(row,int),repr(row)+ ' is not int'
        assert 0<=row and row+2<current.getHeight(), repr(row)+' is not validrow'
        assert isinstance(pixel, tuple) and 0<=pixel[0]<=255 and 0<=pixel[1]<=255
        assert 0<=pixel[2]<=255, repr(pixel) +' is not valid'
        
        for col in range(current.getWidth()):
            current.setPixel(row,   col, pixel)
            current.setPixel(row+1, col, pixel)
            current.setPixel(row+2, col, pixel)
            
            
    def _drawVBar(self, col, pixel):
        """
        Draws a vertical bar on the current image at the given column.
        
        This method draws a vertical 3-pixel-wide bar at the given column of the current
        image. This means that the bar includes the pixels col, col+1, col+2, and col+3.
        The bar uses the color given by the pixel value.
        
        Parameter col: The start of the column to draw the bar
        Precondition: col is an int, with 0 <= col  &&  col+3 < image width
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        """
        current = self.getCurrent()
        assert isinstance(col,int),repr(col)+ ' is not int'
        assert 0<=col and col+3<current.getWidth(), repr(col) +' is not valid col'
        assert isinstance(pixel, tuple) and 0<=pixel[0]<=255 and 0<=pixel[1]<=255
        assert 0<=pixel[2]<=255, repr(pixel) +' is not valid'

        for row in range(current.getHeight()):
            current.setPixel(row,   col, pixel)
            current.setPixel(row, col+1, pixel)
            current.setPixel(row, col+2, pixel)
            current.setPixel(row, col+3, pixel)
       
            
    def _decode_pixel(self, pos):
        """
        Returns: the number n that is hidden in pixel pos of the current image.
        
        This function assumes that the value was a 3-digit number encoded as the
        last digit in each color channel (e.g. red, green and blue).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        assert isinstance(pos,int) and 0<=pos<self.getCurrent().getLength(), repr(
            pos) +'is not valid pos'
        rgb = self.getCurrent().getFlatPixel(pos)
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        return  (red % 10) * 100  +  (green % 10) * 10  +  blue % 10
    
    
    def _encode_pixel(self, pos, c):
        """
        Encodes the character c at pixel pos of the current image. 
        
        c corresponds to a 3-digit number encoded as the
        last digit in each color channel (e.g. red, green and blue).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        
        Parameter c: a string of length 1 or a 3 digit int
        Precondition: c is str w length 1 or a int w/ len<= 3
        """
        assert (isinstance(c,str) and len(c)==1) or (
            isinstance(c,int) and len(str(c))<=3), repr(c)+'is not valid c'
        assert isinstance(pos,int) and 0<=pos<self.getCurrent().getLength(), repr(
            pos) +'is not valid pos'
        
        rgb = self.getCurrent().getFlatPixel(pos)
        if (isinstance(c,str)):
            num=ord(c)
        else:
            num=c
        red=rgb[0]//10*10+num//100
        green=rgb[1]//10*10+num//10%10
        blue=rgb[2]//10*10+num%10
        for x in [red,green,blue]:
            if (x>255):
                x=x-10
        pixel=(red,green,blue)
        self.getCurrent().setFlatPixel(pos,pixel)
        
    
    def _distance(self, x1,y1,x2,y2):
        """
        Returns: distance between pixels at col x1 row y1 and col x2 row y2
        
        This function calculates the distance between two pixels at the given
        coordinates
        
        Parameter x1: the col of the first pixel
        Precondition: x1 is an int and is 0<= and less than image width
        Parameter x2: the col of the second pixel
        Precondition: x2 is an int and is 0<= and less than image width
        Parameter y1: the row of the first pixel
        Precondition: y1 is an int and is 0<= and less than image height
        Parameter y2: the row of the second pixel
        Precondition: y2 is an int and is 0<= and less than image height
        """
        current=self.getCurrent()
        assert isinstance(x1,int) and 0<=x1<current.getWidth()
        assert isinstance(x2,int) and 0<=x2<current.getWidth()
        assert isinstance(y1,int) and 0<=y1<current.getHeight()
        assert isinstance(y2,int) and 0<=y2<current.getHeight()
        x=x1-x2
        y=y1-y2
        #y=abs(y)
        #x=abs(x)
        y=y*y
        x=x*x
        #print(x)
        #print(y)
        #x=((x2-x1)^2)
        #y=((y2-y1)^2)
        #print (str(x)+'is x^2')
        #print (str(y)+'is y^2')
        d=math.sqrt(x+y)
        #print (str(d)+'is d')
        return d
    
    
    def _averageStep(self, rowStart,colStart,step):
        """
        Returns: a pixel with the average red, green, and blue values within the
        step
        
        This function averages all of the red, green, and blue values for each
        pixelstep many positions to the right of colStart and below rowStart.
        If rowStart+step>height then it just goes to th edge of the image. The
        same occurs if colstart+step>width
        
        Parameter rowStart: row of starting pixel
        Precondition: int, 0<=rowStart<image height
        
        Parameter colStart: col of starting pixel
        Precondition: int, 0<=rowStart<image width
        
        Parameter step: width and height of block of same color pixels once
        inamge is pixelated
        Precondition: int, 0<step<image height and 0<step<image width
        """
        current=self.getCurrent()
        assert isinstance(rowStart,int) and 0<=rowStart<current.getHeight()
        assert isinstance(colStart,int) and 0<=colStart<current.getWidth()
        #step asserted in pixelate
        
        if (rowStart+step>=current.getHeight()):
            rowrng=range(rowStart,current.getHeight())
        else:
            rowrng=range(rowStart,rowStart+step+1)
        if (colStart+step>=current.getWidth()):
            colrng=range(colStart,current.getWidth())
        else:
            colrng=range(colStart,colStart+step+1)
        avgred=0
        avgblue=0
        avggreen=0
        numPix=0
        for row in rowrng:
            for col in colrng:
                j=current.getPixel(row,col)
                avgred=avgred+j[0]
                avggreen=avggreen+j[1]
                avgblue=avgblue+j[2]
                numPix=numPix+1
        #numPix=(current.getHeight()-1        
        red=int(round(avgred/numPix))
        green=int(round(avggreen/numPix))
        blue=int(round(avgblue/numPix))
        rgb=(red,green,blue)
        return rgb
    
    
    def _setPixAvg(self,rowStart,colStart,step,pixel):
        """
        sets all pixel values in step to average rgb vals
        
        This function sets all of the red, green, and blue values for each pixel
        step many positions to the right of colStart and below rowStart to the average red,
        green, and blue values. If rowStart+step
        >height then it just goes to th edge of the image. The same occurs if colstart+step
        >width
        Parameter pixel: pixel w/ average red, green and blue vals
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        
        Parameter rowStart: row of starting pixel
        Precondition: int, 0<=rowStart<image height
        
        Parameter colStart: col of starting pixel
        Precondition: int, 0<=rowStart<image width
        
        Parameter step: width and height of block of same color pixels once inamge is
        pixelated
        Precondition: int, 0<step<image height and 0<step<image width
        """
        current=self.getCurrent()
        assert isinstance(rowStart,int) and 0<=rowStart<current.getHeight()
        assert isinstance(colStart,int) and 0<=colStart<current.getWidth()
        #step asserted in pixelate
        assert isinstance(pixel, tuple) and 0<=pixel[0]<=255 and 0<=pixel[1]<=255
        assert 0<=pixel[2]<=255

        
        if (rowStart+step>=current.getHeight()):
            rowrng=range(rowStart,current.getHeight())
        else:
            rowrng=range(rowStart,rowStart+step+1)
        if (colStart+step>=current.getWidth()):
            colrng=range(colStart,current.getWidth())
        else:
            colrng=range(colStart,colStart+step+1)
        
        for row in rowrng:
            for col in colrng:
                current.setPixel(row,col,pixel)
        
    