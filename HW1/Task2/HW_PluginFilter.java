package my_plugins;

import ij.*;
import ij.plugin.filter.PlugInFilter;
import ij.process.*;
import ij.plugin.*;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

public class HW_PluginFilter implements PlugInFilter {
    ImagePlus imagePlus;
    public int setup(String arg, ImagePlus imagePlus) {
        this.imagePlus = imagePlus;
        return DOES_ALL;
    }

    public void run(ImageProcessor ip) {
        int width = ip.getWidth();
        int height = ip.getHeight();

        // dividing the image into left and right panels
        int leftWidth = width / 2;
        int rightWidth = width - leftWidth;

        // swapping the left and right panels horizontally
        swapLeftRight(ip, leftWidth, rightWidth);

        // dividing the image into top and bottom panels
        int topHeight = height / 2;
        int bottomHeight = height - topHeight;

        // swapping the top and bottom panels vertically
        swapTopBottom(ip, topHeight, bottomHeight);

        IJ.save(imagePlus, "copy.png");
    }

    private void swapLeftRight(ImageProcessor ip, int leftWidth, int rightWidth) {
        for (int y = 0; y < ip.getHeight(); y++) {
            for (int x = 0; x < leftWidth; x++) {
                int leftPixel = ip.getPixel(x, y);
                int rightPixel = ip.getPixel(rightWidth + x, y);

                ip.putPixel(x, y, rightPixel);
                ip.putPixel(rightWidth + x, y, leftPixel);
            }
        }
    }

    private void swapTopBottom(ImageProcessor ip, int topHeight, int bottomHeight) {
        for (int x = 0; x < ip.getWidth(); x++) {
            for (int y = 0; y < topHeight; y++) {
                int topPixel = ip.getPixel(x, y);
                int bottomPixel = ip.getPixel(x, bottomHeight + y);

                ip.putPixel(x, y, bottomPixel);
                ip.putPixel(x, bottomHeight + y, topPixel);
            }
        }
    }
}
