package vault;
import java.io.*;
import java.nio.file.*;
import java.util.List;

public class VaultManager {
    public static void main(String[] args) {
        try {
            // Read all lines from the bridge file
            Path path = Paths.get("data/sensitive_raw.txt");
            List<String> lines = Files.readAllLines(path);

            if (lines.size() < 2) {
                System.out.println("❌ Error: Bridge file is incomplete.");
                return;
            }

            // Line 0 is the Name, everything else is the Content
            String userName = lines.get(0);
            String content = String.join("\n", lines.subList(1, lines.size()));

            // Create and save the secure object
            Guardian myVault = new Guardian(content, userName);
            ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("data/shadow_vault.ser"));
            out.writeObject(myVault);
            out.close();
            
            System.out.println("🔒 ShadowVault Synced for user: " + userName);

        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}