import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.file.*;

public class Server {
    public static void main(String[] args) throws IOException {
        // stvori posluzitelj koji slusa na portu:8000
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        server.createContext("/", new MyHandler());
        server.setExecutor(null);
        server.start();
        System.out.println("Server running on http://localhost:8000");
    }

    // poziva se pri svakom dolaznom HTTP zahtjevu, GET
    static class MyHandler implements HttpHandler {
        public void handle(HttpExchange t) throws IOException {
            String uri = t.getRequestURI().getPath();
            if (uri.equals("/"))
                uri = "/index.html";
            Path path = Paths.get(".", uri);

            if (!Files.exists(path)) {
                String response = "404 Not Found";
                t.sendResponseHeaders(404, response.length());
                OutputStream os = t.getResponseBody();
                os.write(response.getBytes());
                os.close();
                return;
            }

            byte[] bytes = Files.readAllBytes(path);
            String contentType = "text/html";
            if (uri.endsWith(".css"))
                contentType = "text/css";
            else if (uri.endsWith(".js"))
                contentType = "application/javascript";

            // slanje HTTP odgovora
            t.getResponseHeaders().add("Content-Type", contentType);
            t.sendResponseHeaders(200, bytes.length);
            OutputStream os = t.getResponseBody();
            os.write(bytes);
            os.close();
        }
    }
}