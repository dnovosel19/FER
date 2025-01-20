package opp.DTO;

public class LocationDTO {
    private Integer id;
    private String name;
    private String coordinates;

    public LocationDTO() {
    }

    public LocationDTO(Integer id, String name, String coordinates) {
        this.id = id;
        this.name = name;
        this.coordinates = coordinates;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCoordinates() {
        return coordinates;
    }

    public void setCoordinates(String coordinates) {
        this.coordinates = coordinates;
    }

    @Override
    public String toString() {
        return "LocationDTO{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", coordinates='" + coordinates + '\'' +
                '}';
    }
}
