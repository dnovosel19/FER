package opp.services;

import opp.DTO.AppointmentDTO;
import opp.DTO.BloodSupplyDTO;
import opp.DTO.OrganizationDTO;
import opp.domain.Organization;

import java.util.List;
import java.util.Optional;

public interface OrganizationService {
    String registerOrganization(OrganizationDTO organizationDTO);
    List<OrganizationDTO> getAllOrganizations();

    OrganizationDTO getOrganizationById(Long organizationId);

    List<BloodSupplyDTO> getBloodSuppliesForOrganization(Long organizationId);

    List<AppointmentDTO> getAvailableAppointmentsForOrganization(Long organizationId);

    Optional<Organization> findByUsername(String username);

    Organization fetch(long donorId);

    Optional<Organization> findById(long groupId);

}
