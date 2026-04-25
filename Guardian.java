package vault;
import java.io.Serializable;

public class Guardian implements Serializable {
    private String sensitiveData;
    private String owner;

    public Guardian(String sensitiveData, String owner) {
        this.sensitiveData = sensitiveData;
        this.owner = owner;
    }

    // These are the "Getter" methods the Unlocker is looking for:
    public String getSensitiveData() {
        return sensitiveData;
    }

    public String getOwner() {
        return owner;
    }
}