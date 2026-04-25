package vault;
import java.io.*;

public class VaultUnlocker {
    public static void main(String[] args) {
        try {
            // 1. Open the serialized vault file
            ObjectInputStream in = new ObjectInputStream(new FileInputStream("data/shadow_vault.ser"));
            
            // 2. Read the object and cast it back to Guardian
            Guardian retrievedVault = (Guardian) in.readObject();
            in.close();

            // 3. Display the data in the same format the terminal expects
            System.out.println("? Vault Unlocked Successfully!");
            System.out.println("Original Data: " + retrievedVault.getSensitiveData());
            System.out.println("Stored by: " + retrievedVault.getOwner());
            // Note: If you added a timestamp to Guardian, you can print it here too
            
        } catch (FileNotFoundException e) {
            System.err.println("❌ Error: Vault file 'shadow_vault.ser' not found. Seal a file first!");
            System.exit(1);
        } catch (Exception e) {
            System.err.println("❌ Error during decryption: " + e.getMessage());
            System.exit(1);
        }
    }
}
