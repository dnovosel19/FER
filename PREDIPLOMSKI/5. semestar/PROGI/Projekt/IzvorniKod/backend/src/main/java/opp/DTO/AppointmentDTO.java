package opp.DTO;

import java.time.LocalDate;

public class AppointmentDTO {
    private Integer id;
    private LocalDate startTime;
    private LocalDate endTime;
    private Integer donationActionId;
    private LocationDTO location;

    public AppointmentDTO() {
    }

    public AppointmentDTO(Integer id, LocalDate startTime, LocalDate endTime, Integer donationActionId, LocationDTO location) {
        this.id = id;
        this.startTime = startTime;
        this.endTime = endTime;
        this.donationActionId = donationActionId;
        this.location = location;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public LocalDate getStartTime() {
        return startTime;
    }

    public void setStartTime(LocalDate startTime) {
        this.startTime = startTime;
    }

    public LocalDate getEndTime() {
        return endTime;
    }

    public void setEndTime(LocalDate endTime) {
        this.endTime = endTime;
    }

    public Integer getDonationActionId() {
        return donationActionId;
    }

    public void setDonationActionId(Integer donationActionId) {
        this.donationActionId = donationActionId;
    }

    public LocationDTO getLocation() {
        return location;
    }

    public void setLocation(LocationDTO location) {
        this.location = location;
    }

    @Override
    public String toString() {
        return "AppointmentDTO{" +
                "id=" + id +
                ", startTime=" + startTime +
                ", endTime=" + endTime +
                ", donationActionId=" + donationActionId +
                ", location=" + location +
                '}';
    }
}