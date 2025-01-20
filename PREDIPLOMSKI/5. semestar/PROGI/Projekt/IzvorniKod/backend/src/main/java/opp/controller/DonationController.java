package opp.controller;

import jakarta.transaction.Transactional;
import opp.DTO.BloodDonorDTO;
import opp.DTO.DonationDTO;
import opp.DTO.LocationDTO;
import opp.DTO.OrganizationDTO;
import opp.dao.*;
import opp.domain.*;
import opp.services.impl.DonationServiceJpa;
import opp.services.impl.OrganizationServiceJpa;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/donation")
public class DonationController {

    @Autowired
    private DonationsRepository donationRepository;
    @Autowired
    private BloodDonorRepository bloodDonorRepository;
    @Autowired
    private OrganizationRepository organizationRepository;
    @Autowired
    private BloodGroupRepository bloodGroupRepository;
    @Autowired
    private OrganizationServiceJpa organizationServices;
    @Autowired
    private DonationServiceJpa donationServiceJpa;
    @Autowired
    private DonorAppointmentRepository donorAppointmentRepository;

    @PostMapping("/apply")
    public ResponseEntity<?> applyForDonation(@RequestBody Map<String, Object> requestBody) {
        try {
            System.out.println("Received data: " + requestBody);

            String donorUsername = requestBody.get("donorUsername").toString();
            Long organizationId = Long.valueOf(requestBody.get("organizationId").toString());
            System.out.println("Received request with donorUsername: " + donorUsername);

            Donor bloodDonor = bloodDonorRepository.findByUsername(donorUsername);
            boolean hasPreviousDonations = donationRepository.existsByDonor(bloodDonor);

            if (bloodDonor == null) {
                System.err.println("Blood donor not found for username: " + donorUsername);
                return ResponseEntity.badRequest().body("Blood donor not found for username: " + donorUsername);
            }

            System.out.println("Blood donor found: " + bloodDonor.toString());

            Organization organization = organizationRepository.findById(organizationId)
                    .orElseThrow(() -> new RuntimeException("Organization not found for id: " + organizationId));

            System.out.println("Organization found: " + organization);

            System.out.println("Processing the donation application...");
            String selectedBloodGroup = Objects.toString(requestBody.get("selectedBloodGroup"), "");
            System.out.println("Selected Blood Group: " + selectedBloodGroup);

            BloodGroup bloodGroup = bloodGroupRepository.findByBloodType(selectedBloodGroup);

            if (bloodGroup == null) {
                System.err.println("Blood group not found: " + selectedBloodGroup);
                return ResponseEntity.badRequest().body("Blood group not found: " + selectedBloodGroup);
            }

            System.out.println("Organization Location: " + organization.getLocation());
            System.out.println("Blood group: " + bloodGroup.toString());
            Donation donation = new Donation();
            donation.setDonor(bloodDonor);
            donation.setOrganization(organization);
            donation.setBloodGroup(bloodGroup);
            donation.setLocation(organization.getLocation());
            donation.setTime(LocalDate.now());
            donationRepository.save(donation);
            if (hasPreviousDonations) {
                donationServiceJpa.updateBloodSupplies(organizationId, donorUsername, 50);
            }

            Long bloodDonorId = Long.valueOf(bloodDonor.getId());
            System.out.println("Donation application successful. Blood donor ID: " + bloodDonorId);

            return ResponseEntity.ok(Map.of("bloodDonorId", bloodDonorId, "message", "Donation application successful"));
        } catch (Exception e) {
            System.err.println("Error processing donation application: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error processing donation application");
        }
    }


    @PostMapping("/rejectApplication")
    public ResponseEntity<?> rejectApplication(@RequestBody Map<String, Object> requestBody) {
        try {
            Long organizationId = Long.parseLong(requestBody.get("organizationId").toString());
            Long donationId = Long.parseLong(requestBody.get("donationId").toString());
            String donorUsername = requestBody.get("donorUsername").toString();
            System.out.println("id donacije: " + donationId);

             donationServiceJpa.rejectDonorApplication(organizationId, donorUsername, donationId);

            return ResponseEntity.ok("Application rejected successfully");
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error rejecting application");
        }
    }

    @PostMapping("/acceptApplication")
    public ResponseEntity<?> acceptDonationApplication(@RequestBody Map<String, Object> request) {
        try {
            Long organizationId = Long.parseLong(request.get("organizationId").toString());
            String donorUsername = request.get("donorUsername").toString();
            Long donorId = Long.parseLong(request.get("donorId").toString());
            Long appointmentId = Long.parseLong(request.get("appointmentId").toString());
            Long donationId = Long.parseLong(request.get("donationId").toString());

            System.out.println("Donation application accepted - Organization ID: " + organizationId +
                    ", Donor ID: " + donorId + ", Appointment ID: " + appointmentId + ", Donor Username: " + donorUsername + " Donation ID: " + donationId);

            donationServiceJpa.acceptDonorApplication(organizationId, donorUsername, donorId, appointmentId, donationId);

            System.out.println("Updating blood supplies - Organization ID: " + organizationId +
                    ", Donor ID: " + donorId + ", Appointment ID: " + appointmentId + ", Donor Username: " + donorUsername + ", Amount to add: 50");
            System.out.println("Application accepted successfully");

            return ResponseEntity.ok("Application accepted successfully");
        } catch (Exception e) {
            e.printStackTrace();
            System.err.println("Error accepting application");

            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error accepting application");
        }
    }
    @PostMapping("/removeApplication")
    @Transactional
    public ResponseEntity<?> removeDonationApplication(@RequestBody Map<String, Object> requestBody) {
        try {
            Long donationId = Long.valueOf(requestBody.get("donationId").toString());

            System.out.println("Received request to remove donation application: Donation ID: " + donationId);

            Donation donation = donationRepository.findById(donationId)
                    .orElseThrow(() -> new RuntimeException("Donation not found for id: " + donationId));

            donationRepository.delete(donation);

            System.out.println("Donation application removed successfully.");

            return ResponseEntity.ok(Map.of("message", "Donation application removed"));
        } catch (Exception e) {
            System.err.println("Error removing donation application: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Error removing donation application");
        }
    }

    @GetMapping("/reservedDonations/{donorId}")
    public ResponseEntity<List<DonationDTO>> getReservedDonationsForDonor(@PathVariable Long donorId) {
        try {
            List<Donation> reservedDonations = donationRepository.findReservedDonationsByDonorId(donorId);

            List<DonationDTO> donationDTOs = reservedDonations.stream()
                    .map(donation -> {
                        DonationDTO donationDTO = new DonationDTO();
                        donationDTO.setId(donation.getId());
                        donationDTO.setTime(donation.getTime().toString());
                        donationDTO.setBloodType(donation.getBloodGroup().getBloodType());

                        LocationDTO locationDTO = new LocationDTO();
                        locationDTO.setId(donation.getLocation().getId());
                        locationDTO.setName(donation.getLocation().getName());
                        locationDTO.setCoordinates(donation.getLocation().getCoordinates());
                        donationDTO.setLocation(locationDTO);

                        OrganizationDTO organizationDTO = new OrganizationDTO();
                        organizationDTO.setId(donation.getOrganization().getId());
                        organizationDTO.setNaziv(donation.getOrganization().getNaziv());
                        donationDTO.setOrganization(organizationDTO);

                        return donationDTO;
                    })
                    .collect(Collectors.toList());

            return ResponseEntity.ok(donationDTOs);
        } catch (Exception e) {
            System.err.println("Error retrieving reserved donations: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }
    @GetMapping("/appliedDonors/{organizationId}")
    public ResponseEntity<List<BloodDonorDTO>> getAppliedDonorsForOrganization(@PathVariable Long organizationId, Integer reservationStatus) {
        try {
            List<BloodDonorDTO> appliedDonors = donationServiceJpa.getAppliedDonorsForOrganization(organizationId);

            appliedDonors = appliedDonors.stream()
                    .filter(donor -> {
                        DonorAppointment donorAppointment = donorAppointmentRepository.findByDonor_Id(donor.getId());
                        return donorAppointment == null || !donorAppointment.getStatus().equals(1);
                    })
                    .collect(Collectors.toList());

            return ResponseEntity.ok(appliedDonors);
        } catch (Exception e) {
            System.err.println("Error retrieving applied donors for organization: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }

    @GetMapping("/appliedDonations/{organizationId}")
    public ResponseEntity<List<DonationDTO>> getAppliedDonationsForOrganization(@PathVariable Long organizationId) {
        try {
            List<Donation> appliedDonations = donationServiceJpa.getAppliedDonationsForOrganization(organizationId);

            List<DonationDTO> donationDTOs = appliedDonations.stream()
                    .map(donation -> {
                        DonationDTO donationDTO = new DonationDTO();
                        donationDTO.setId(donation.getId());
                        donationDTO.setTime(donation.getTime().toString());
                        donationDTO.setBloodType(donation.getBloodGroup().getBloodType());

                        LocationDTO locationDTO = new LocationDTO();
                        locationDTO.setId(donation.getLocation().getId());
                        locationDTO.setName(donation.getLocation().getName());
                        locationDTO.setCoordinates(donation.getLocation().getCoordinates());
                        donationDTO.setLocation(locationDTO);

                        OrganizationDTO organizationDTO = new OrganizationDTO();
                        organizationDTO.setId(donation.getOrganization().getId());
                        organizationDTO.setNaziv(donation.getOrganization().getNaziv());
                        donationDTO.setOrganization(organizationDTO);

                        return donationDTO;
                    })
                    .collect(Collectors.toList());

            return ResponseEntity.ok(donationDTOs);
        } catch (Exception e) {
            System.err.println("Error retrieving applied donations for organization: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }
    @GetMapping("/donationCount")
    public ResponseEntity<List<Map<Donor, Object>>> getDonationsCount() {
        try {
            List<Map<Donor, Object>> donationsCountList = donationRepository.countDonationsPerDonor();

            System.out.println("Successfully retrieved donations count per donor");

            return ResponseEntity.ok(donationsCountList);
        } catch (Exception e) {
            System.err.println("Error retrieving donations count per donor: " + e.getMessage());
            e.printStackTrace();

            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }
    @GetMapping("/exists")
    public ResponseEntity<List<DonationDTO>> getDonationsWithoutAppointments() {
        try {
            List<Donation> donations = donationRepository.findAll();

            List<DonationDTO> donationsWithoutAppointments = donations.stream()
                    .filter(donation -> donorAppointmentRepository.existsByDonor_Id(donation.getDonor().getId()))
                    .map(this::convertToDTO)
                    .collect(Collectors.toList());

            System.out.println("All Donations: " + donations);
            System.out.println("Donations Without Appointments: " + donationsWithoutAppointments);
            System.out.println(ResponseEntity.ok(donationsWithoutAppointments));
            return ResponseEntity.ok(donationsWithoutAppointments);
        } catch (Exception e) {
            e.printStackTrace();
            System.err.println("Error getting donations without appointments: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Collections.emptyList());
        }
    }

    private DonationDTO convertToDTO(Donation donation) {
        DonationDTO dto = new DonationDTO();
        dto.setId(donation.getId());
        return dto;
    }


}
