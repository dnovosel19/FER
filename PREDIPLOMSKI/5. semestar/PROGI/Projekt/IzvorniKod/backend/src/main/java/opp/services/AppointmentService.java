package opp.services;

import opp.domain.Appointment;

import java.util.List;

public interface AppointmentService {
    List<Appointment> listAll();

    public Appointment createAppointment(Appointment appointment);
}
