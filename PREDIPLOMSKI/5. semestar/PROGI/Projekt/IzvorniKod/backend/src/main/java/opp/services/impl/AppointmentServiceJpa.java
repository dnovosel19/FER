package opp.services.impl;

import opp.dao.AppointmentRepository;
import opp.dao.BloodDonorRepository;
import opp.domain.Appointment;
import opp.services.AppointmentService;
import opp.services.RequestDeniedException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;

import java.util.List;


@Service
public class AppointmentServiceJpa implements AppointmentService {
    @Autowired
    private AppointmentRepository appointmentRepo;

    public List<Appointment> listAll(){
        return appointmentRepo.findAll();
    }

    public Appointment createAppointment(Appointment appointment){
        Assert.notNull(appointment, "Appointment object must be given.");
        Assert.isNull(appointment.getId(), "Appointment ID must be null.");
        // Dodati po cemu jos zelimo razlikovati nase termine
        //if(appointmentRepo.countByAppointmentTime(appointment.getAppointmentTime())>0){
        //    throw new RequestDeniedException("Appointment with Id " + appointment.getId() + " exists.");
        //}
        return appointmentRepo.save(appointment);
    }
}
