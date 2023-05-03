import java.io.BufferedReader; 
import java.io.InputStreamReader; 
import java.net.HttpURLConnection; 
import java.net.URL;

public class GetSubmitter {
     public static void main(String[] args) {
         try {
         // Create URL 
         URL url = new URL("http://localhost/search/?code=600352&days=100&date=20230125"); // Create connection 
         HttpURLConnection con = (HttpURLConnection) 
         url.openConnection(); 
         // Set request method 
         con.setRequestMethod("GET"); 
         // Get response 
         BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream())); 
         String inputLine; 
         StringBuffer response = new StringBuffer(); 
         while ((inputLine = in.readLine()) != null) {
             response.append(inputLine);
             } in.close(); 
             // Print response 
             System.out.println(response.toString()); 
            } catch (Exception ex) { 
                ex.printStackTrace(); 
            } 
        } 
    }