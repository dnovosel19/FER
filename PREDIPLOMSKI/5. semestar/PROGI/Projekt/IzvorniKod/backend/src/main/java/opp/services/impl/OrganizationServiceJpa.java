package opp.services.impl;

import opp.DTO.*;
import opp.dao.*;
import opp.domain.*;
import opp.services.EntityMissingException;
import opp.services.OrganizationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.*;
import java.util.stream.Collectors;

@Service
public class OrganizationServiceJpa implements OrganizationService {

    @Autowired
    private OrganizationRepository organizationRepository;

    @Autowired
    private BloodDonorRepository bloodDonorRepository;

    @Autowired
    private OrganizationTypeRepository organizationTypeRepository;

    @Autowired
    private BloodSuppliesRepository bloodSuppliesRepository;

    @Autowired
    private LocationRepository locationRepository;

    @Autowired
    PasswordEncoder encoder;

    @Override
    public String registerOrganization(OrganizationDTO organizationDTO) {
        try {
            Organization existingOrganizationUsername = organizationRepository.findByAdminUsername(organizationDTO.getAdminUsername());
            System.out.println("Received data: " + organizationDTO.toString());
            Donor existingDonorUsername = bloodDonorRepository.findByUsername(organizationDTO.getAdminUsername());

            if (existingOrganizationUsername != null && existingDonorUsername != null) {
                return "Username already exists";
            }
            Organization organization = new Organization(
                    organizationDTO.getAdminUsername(),
                    encoder.encode(organizationDTO.getAdminPassword()),
                    organizationDTO.getAdminName(),
                    organizationDTO.getAdminSurname(),
                    organizationDTO.getNaziv(),
                    locationRepository.findById(organizationDTO.getLocationId().longValue()).orElseThrow(
                            () -> new EntityMissingException(Location.class, organizationDTO.getLocationId())
                    ),
                    organizationTypeRepository.findById(organizationDTO.getOrganizationTypeId().longValue()).orElseThrow(
                            () -> new EntityMissingException(Location.class, organizationDTO.getOrganizationTypeId())
                    )
            );
            organizationRepository.save(organization);
            return "Registration successful for user " + organizationDTO.getAdminUsername();
        } catch (Exception e) {
            e.printStackTrace();
            return "Error during registration";
        }
    }

    @Override
    public List<OrganizationDTO> getAllOrganizations() {
        return organizationRepository.findAll().stream()
                .map(organization -> new OrganizationDTO(
                        organization.getId(),
                        organization.getAdminUsername(),
                        organization.getAdminPassword(),
                        organization.getAdminName(),
                        organization.getAdminSurname(),
                        organization.getLocation().getId(),
                        organization.getOrganizationType().getId(),
                        organization.getNaziv()
                ))
                .collect(Collectors.toList());
    }

    @Override
    public OrganizationDTO getOrganizationById(Long organizationId) {
        try {
            Optional<Organization> organizationOptional = organizationRepository.findById(organizationId);

            if (organizationOptional.isPresent()) {
                Organization organization = organizationOptional.get();
                return new OrganizationDTO(
                        organization.getId(),
                        organization.getAdminUsername(),
                        organization.getAdminPassword(),
                        organization.getAdminName(),
                        organization.getAdminSurname(),
                        organization.getLocation().getId(),
                        organization.getOrganizationType().getId(),
                        organization.getNaziv()
                );
            } else {
                System.err.println("Organization not found for ID: " + organizationId);
                return null;
            }
        } catch (Exception e) {
            System.err.println("Error occurred in getOrganizationById");
            e.printStackTrace();
            return null;
        }
    }

    @Override
    public List<BloodSupplyDTO> getBloodSuppliesForOrganization(Long organizationId) {
        try {
            List<BloodSupply> bloodSupplies = bloodSuppliesRepository.findByOrganizationId(organizationId);

            return bloodSupplies.stream()
                    .map(bloodSupply -> new BloodSupplyDTO(
                            bloodSupply.getId(),
                            bloodSupply.getAmount(),
                            bloodSupply.getOrganization().getNaziv(),
                            bloodSupply.getBloodGroup().getBloodType()
                    ))
                    .collect(Collectors.toList());
        } catch (Exception e) {
            System.err.println("Error occurred in getBloodSuppliesForOrganization");
            e.printStackTrace();
            return null;
        }
    }
    @Override
    public List<AppointmentDTO> getAvailableAppointmentsForOrganization(Long organizationId) {
        try {
            Optional<Organization> organizationOptional = organizationRepository.findById(organizationId);

            if (organizationOptional.isPresent()) {
                Organization organization = organizationOptional.get();
                List<AppointmentDTO> appointments = organization.getDonationActions().stream()
                        .flatMap(donationAction -> donationAction.getAppointments().stream())
                        .map(appointment -> {
                            Integer locationId = appointment.getDonationAction().getLocation().getId();

                            return new AppointmentDTO(
                                    appointment.getId(),
                                    appointment.getStartTime(),
                                    appointment.getEndTime(),
                                    appointment.getDonationAction().getId(),
                                    new LocationDTO(locationId, organization.getLocation().getName(), organization.getLocation().getCoordinates())
                            );
                        })
                        .collect(Collectors.toList());

                return appointments;
            } else {
                System.err.println("Organization not found for ID: " + organizationId);
                return Collections.emptyList();
            }
        } catch (Exception e) {
            System.err.println("Error occurred in getAvailableAppointmentsForOrganization");
            e.printStackTrace();
            return Collections.emptyList();
        }
}

    @Override
    public Optional<Organization> findByUsername(String username) {
        return Optional.ofNullable(organizationRepository.findByAdminUsername(username));
    }

    @Override
    public Organization fetch(long donorId) {
        return findById(donorId).orElseThrow(
                () -> new EntityMissingException(Organization.class, donorId)
        );
    }

    @Override
    public Optional<Organization> findById(long groupId) {
        return organizationRepository.findById(groupId);
    }
}
