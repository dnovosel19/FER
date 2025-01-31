package opp.DTO;

public class LoginDTO {
    private String username;
    private Long id;
    private String password;

    public LoginDTO() {

    }

    public LoginDTO(String username, String password, Long id) {
        this.username = username;
        this.password = password;
        this.id = id;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
