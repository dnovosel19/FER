package opp.DTO;

public class BloodDonorDTO {
    private Integer id;

    private String username;

    private String password;

    private String name;

    private String surname;

    private String oib;

    public BloodDonorDTO() {
    }

    public BloodDonorDTO(String username, String password, String name, String surname, String oib) {
        this.username = username;
        this.password = password;
        this.name = name;
        this.surname = surname;
        this.oib = oib;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
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

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSurname() {
        return surname;
    }

    public void setSurname(String surname) {
        this.surname = surname;
    }

    public String getOib() {
        return oib;
    }

    public void setOib(String oib) {
        this.oib = oib;
    }

    @Override
    public String toString() {
        return "BloodDonorDTO{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", password='" + password + '\'' +
                ", name='" + name + '\'' +
                ", surname='" + surname + '\'' +
                ", oib='" + oib + '\'' +
                '}';
    }
}