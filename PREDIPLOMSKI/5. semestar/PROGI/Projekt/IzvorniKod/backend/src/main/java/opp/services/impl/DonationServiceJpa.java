package opp.services.impl;

import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import opp.DTO.BloodDonorDTO;
import opp.dao.*;
import opp.domain.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class DonationServiceJpa {
    @Autowired
    private OrganizationRepository organizationRepository;

    @Autowired
    private DonationsRepository donationRepository;

    @Autowired
    private BloodDonorRepository bloodDonorRepository;
    @Autowired
    private BloodSuppliesRepository bloodSuppliesRepository;
    @Autowired
    private AppointmentRepository appointmentRepository;
    @Autowired
    private DonorAppointmentRepository donorAppointmentRepository;

    public void applyForDonation(Long organizationId, Donor donorDTO) {
        Organization organization = organizationRepository.findById(organizationId)
                .orElseThrow(() -> new EntityNotFoundException("Organization not found"));

        Donor donor = bloodDonorRepository.findByUsername(donorDTO.getUsername());

        Optional<Donation> existingDonation = donationRepository.findByOrganizationAndDonor(organization, donor);

        if (existingDonation.isEmpty()) {
            Donation donation = new Donation();
            donation.setDonor(donor);
            donation.setOrganization(organization);
            donationRepository.save(donation);
            updateBloodSupplies(organizationId, donorDTO.getUsername(), 50);
        }
    }

    public List<BloodDonorDTO> getAppliedDonorsForOrganization(Long organizationId) {
        Organization organization = organizationRepository.findById(organizationId)
                .orElseThrow(() -> new RuntimeException("Organization not found for id: " + organizationId));

        List<Donation> donations = donationRepository.findByOrganization(organization);

        return donations.stream()
                .map(donation -> {
                    Donor donor = donation.getDonor();
                    BloodDonorDTO donorDTO = new BloodDonorDTO();
                    donorDTO.setId(donor.getId());
                    donorDTO.setUsername(donor.getUsername());
                    donorDTO.setPassword(donor.getPassword());
                    donorDTO.setName(donor.getName());
                    donorDTO.setSurname(donor.getSurname());
                    donorDTO.setOib(donor.getOib());
                    return donorDTO;
                })
                .collect(Collectors.toList());
    }

    public void rejectDonorApplication(Long organizationId, String donorUsername, Long donationId) {
        System.out.println("Organization ID: " + organizationId);
        System.out.println("Username: " + donorUsername);
        System.out.println("ID donacije u rejectDonorApplication: " + donationId);
        Donation d = donationRepository.findById(donationId)
                .orElseThrow(() -> new EntityNotFoundException("Organization not found"));

        donationRepository.delete(d);
    }
    public void acceptDonorApplication(Long organizationId, String donorUsername, Long donorId, Long appointmentId, Long donationId) {
        try {
            Donor donor = bloodDonorRepository.findByUsername(donorUsername);
            Donation donation = donationRepository.findById(donationId)
                    .orElseThrow(() -> new EntityNotFoundException("Donation not found for the given organization and donor"));

            donationRepository.save(donation);
            Appointment appointment = appointmentRepository.findById(appointmentId)
                    .orElseThrow(() -> new EntityNotFoundException("Appointment not found"));
            DonorAppointmentId donorAppointmentId = new DonorAppointmentId(donorId.intValue(), appointmentId.intValue());

            DonorAppointment donorAppointment = new DonorAppointment();
            donorAppointment.setId(donorAppointmentId);
            donorAppointment.setDonor(donor);
            donorAppointment.setAppopintment(appointment);
            donorAppointment.setStatus(1);

            donorAppointmentRepository.save(donorAppointment);

            updateBloodSupplies(organizationId, donorUsername, 50);
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("Error accepting donor application");
        }
    }


    public List<Donation> getAppliedDonationsForOrganization(Long organizationId) {
        Organization organization = organizationRepository.findById(organizationId)
                .orElseThrow(() -> new EntityNotFoundException("Organization not found"));

        return donationRepository.findByOrganization(organization);
    }

    @Transactional
    public void updateBloodSupplies(Long organizationId, String donorUsername, int amountToAdd) {
        try {
            Organization organization = organizationRepository.findById(organizationId)
                    .orElseThrow(() -> new EntityNotFoundException("Organization not found"));

            Donor donor = bloodDonorRepository.findByUsername(donorUsername);

            if (donor == null) {
                throw new EntityNotFoundException("Donor not found");
            }

            Donation latestDonation = donationRepository.findTopByDonorOrderByTimeDesc(donor);

            if (latestDonation == null) {
                throw new NoDonationFoundException("No donations found for the donor");
            }

            BloodGroup bloodGroup = latestDonation.getBloodGroup();

            BloodSupply bloodSupply = bloodGroup.getZalihakrvis().stream()
                    .filter(bs -> bs.getOrganization().equals(organization))
                    .findFirst()
                    .orElseThrow(() -> new EntityNotFoundException("Blood supply not found for the given organization and blood group"));

            int newAmount = Math.max(bloodSupply.getAmount() + amountToAdd, 0);
            bloodSupply.setAmount(newAmount);

            bloodSuppliesRepository.save(bloodSupply);

            if (newAmount < 200) {
                System.out.println("Blood supply is below 200 units. Sending notification to users...");
            }

        } catch (NoDonationFoundException e) {
            e.printStackTrace();
            throw new RuntimeException("Error updating blood supplies: " + e.getMessage());
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("Error updating blood supplies");
        }
    }

    public class NoDonationFoundException extends RuntimeException {
        public NoDonationFoundException(String message) {
            super(message);
        }
    }
}