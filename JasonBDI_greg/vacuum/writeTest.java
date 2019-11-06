import java.io.FileWriter; //for writing csv file
import java.io.PrintWriter; //for writing csv file
import java.io.IOException; //for file writing errors 
import java.io.BufferedWriter;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class writeTest {

    public static void main(String[] args) {

        String content = "This is the content to write into file\n";

        // If the file doesn't exists, create and write to it
		// If the file exists, truncate (remove all content) and write to it
        try (FileWriter writer = new FileWriter("app.log");
             BufferedWriter bw = new BufferedWriter(writer)) {

            bw.write(content);

        } catch (IOException e) {
            System.err.format("IOException: %s%n", e);
        }

    }
}
