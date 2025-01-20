package opp.DTO;

public class ApplyForDonationDTO {
    private Long donorId;
    private Long organizationId;

    public ApplyForDonationDTO(Long donorId, Long organizationId) {
        this.donorId = donorId;
        this.organizationId = organizationId;
    }

    public Long getDonorId() {
        return donorId;
    }

    public void setDonorId(Long donorId) {
        this.donorId = donorId;
    }

    public Long getOrganizationId() {
        return organizationId;
    }

    public void setOrganizationId(Long organizationId) {
        this.organizationId = organizationId;
    }

    @Override
    public String toString() {
        return "ApplyForDonationDTO{" +
                "donorId=" + donorId +
                ", organizationId=" + organizationId +
                '}';
    }
}
