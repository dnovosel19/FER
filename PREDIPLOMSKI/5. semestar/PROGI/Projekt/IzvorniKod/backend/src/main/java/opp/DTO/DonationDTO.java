package opp.DTO;


public class DonationDTO {
    private Integer id;
    private String time;
    private String bloodType;
    private String organizationName;
    private LocationDTO location;
    private OrganizationDTO organization;
    private Integer iddonor;
    public DonationDTO() {
    }

    public DonationDTO(Integer id, String time, String bloodType, String organizationName, LocationDTO location) {
        this.id = id;
        this.time = time;
        this.bloodType = bloodType;
        this.organizationName = organizationName;
        this.location = location;
    }

//    public DonationDTO(Donation donation) {
//        this.id = donation.getId();
//        this.time = donation.getTime().toString();
//        this.bloodType = donation.getBloodGroup().getBloodType();
//        this.organizationName = donation.getOrganization().getAdminName();
//        this.location = donation.getLocation();
//    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public String getBloodType() {
        return bloodType;
    }

    public void setBloodType(String bloodType) {
        this.bloodType = bloodType;
    }

    public String getOrganizationName() {
        return organizationName;
    }

    public void setOrganizationName(String organizationName) {
        this.organizationName = organizationName;
    }

    public LocationDTO getLocation() {
        return location;
    }

    public void setLocation(LocationDTO location) {
        this.location = location;
    }

    public OrganizationDTO getOrganization() {
        return organization;
    }

    public void setOrganization(OrganizationDTO organization) {
        this.organization = organization;
    }

    @Override
    public String toString() {
        return "DonationDTO{" +
                "id=" + id +
                ", time='" + time + '\'' +
                ", bloodType='" + bloodType + '\'' +
                ", organizationName='" + organizationName + '\'' +
                ", location='" + location + '\'' +
                '}';
    }
}
