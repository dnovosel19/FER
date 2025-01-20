package opp.domain;

import jakarta.persistence.*;

@Entity
@Table(name = "donortermin")
public class DonorAppointment {
    @EmbeddedId
    private DonorAppointmentId id;

    @ManyToOne
    @MapsId("studentId")
    @JoinColumn(name = "iddonor")
    Donor donor;

    @ManyToOne
    @MapsId("courseId")
    @JoinColumn(name = "idtermin")
    Appointment appopintment;

    @Column(name = "statusrezervacije", nullable = false)
    private Integer status;

    public DonorAppointment() {
    }

    public DonorAppointment(DonorAppointmentId id, Donor donor, Integer status) {
        this.id = id;
        this.donor = donor;
        this.status = status;
    }

    public DonorAppointmentId getId() {
        return id;
    }

    public void setId(DonorAppointmentId id) {
        this.id = id;
    }

    public Donor getDonor() {
        return donor;
    }

    public void setDonor(Donor donor) {
        this.donor = donor;
    }

    public Appointment getAppopintment() {
        return appopintment;
    }

    public void setAppopintment(Appointment appopintment) {
        this.appopintment = appopintment;
    }

    public Integer getStatus() {
        return status;
    }

    public void setStatus(Integer status) {
        this.status = status;
    }
}