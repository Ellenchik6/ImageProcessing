package my_plugins;

import ij.*;
import ij.process.*;
import ij.plugin.*;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;


public class HW_Plugin implements PlugIn {
	@Override
	public void run(String s) {
		String courseFile = "C:/Users/ellen/Desktop/sta-f-83.crs";
		String studentFile = "C:/Users/ellen/Desktop/sta-f-83.stu";
		// number of courses N
		int numOfCourses = N(courseFile);
		// creating a new BinaryProcessor of size N x N and filling it with white
		ImageProcessor imageProcessor = new BinaryProcessor(new ByteProcessor(numOfCourses, numOfCourses));
		imageProcessor.setColor(255);
		imageProcessor.fill();
		List<int[]> c = getCP(studentFile);
		for (int[] pair : c) {
			int x = pair[0];
			int y = pair[1];
			imageProcessor.putPixel(x, y, 0);
		}

		ImagePlus imagePlus = new ImagePlus("sta-f-83", imageProcessor);
		IJ.save(imagePlus, "sta-f-83.png");
	}

	private int N(String courseFile) {
		int numOfCourses = -1;
		try (BufferedReader br = new BufferedReader(new FileReader(courseFile))) {
			String line;
			while ((line = br.readLine()) != null) {
				line = line.trim();
				if (!line.isEmpty()) {
					String[] s = line.split(" ");
					if (s.length > 0) {
						numOfCourses = Integer.parseInt(s[0]);
					}
				}
			}
		} catch (Exception e) {
			numOfCourses = -1;
		}
		return numOfCourses;
	}

	private List<int[]> getCP(String studentFile) {
		List<int[]> cp = new ArrayList<>();
		try (BufferedReader br = new BufferedReader(new FileReader(studentFile))) {
			String line;
			while ((line = br.readLine()) != null) {
				String[] tokens = line.split(" ");
				if (tokens.length > 1) {
					for (int i = 0; i < tokens.length - 1; i++) {
						int firstCourse = Integer.parseInt(tokens[i]);
						for (int j = i + 1; j < tokens.length; j++) {
							int secondCourse = Integer.parseInt(tokens[j]);
							if (firstCourse != secondCourse) {
								cp.add(new int[]{firstCourse, secondCourse});
							}
						}
					}
				}
			}
		} catch (Exception e) {
			return null;
		}
		return cp;
	}
}
