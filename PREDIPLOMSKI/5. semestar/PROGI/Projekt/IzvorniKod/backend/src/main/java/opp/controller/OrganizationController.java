package opp.controller;

import opp.DTO.AppointmentDTO;
import opp.DTO.BloodSupplyDTO;
import opp.DTO.OrganizationDTO;
import opp.services.OrganizationService;
import opp.services.RequestDeniedException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.annotation.Secured;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/organization")
public class OrganizationController {

    @Autowired
    private OrganizationService organizationService;

    @PostMapping(path = "/registerOrganization")
    public ResponseEntity<String> registerOrganization(@RequestBody OrganizationDTO organizationDTO) {
        String registeredOrganization = organizationService.registerOrganization(organizationDTO);

        if (registeredOrganization.startsWith("Username is already taken")) {
            return new ResponseEntity<>(registeredOrganization, HttpStatus.BAD_REQUEST);
        } else if (registeredOrganization.startsWith("Name is already taken")) {
            return new ResponseEntity<>(registeredOrganization, HttpStatus.BAD_REQUEST);
        } else if (registeredOrganization.startsWith("Registration successful")) {
            return new ResponseEntity<>(registeredOrganization, HttpStatus.OK);
        } else {
            return new ResponseEntity<>(registeredOrganization, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/allOrganizations")
    public ResponseEntity<List<OrganizationDTO>> getAllOrganizations() {
        try {
            System.out.println("Request received for getAllOrganizations");

            List<OrganizationDTO> organizations = organizationService.getAllOrganizations();

            System.out.println("Returned " + organizations.size() + " organizations:");

            for (OrganizationDTO organization : organizations) {
                System.out.println(organization);
            }

            return new ResponseEntity<>(organizations, HttpStatus.OK);
        } catch (Exception e) {
            System.err.println("Error occurred in getAllOrganizations");
            e.printStackTrace();
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    @Secured("ROLE_ORGANIZATION")
    @GetMapping("/{organizationId}")
    public ResponseEntity<OrganizationDTO> getOrganizationById(@PathVariable Long organizationId, @AuthenticationPrincipal CustomUserDetails u) {
        checkAllowed(organizationId, u.getUsername());
        try {
            System.out.println("Request received for getOrganizationById: " + organizationId);

            OrganizationDTO organization = organizationService.getOrganizationById(organizationId);

            if (organization != null) {
                System.out.println("Returned organization details: " + organization);
                return new ResponseEntity<>(organization, HttpStatus.OK);
            } else {
                System.err.println("Organization not found for ID: " + organizationId);
                return new ResponseEntity<>(HttpStatus.NOT_FOUND);
            }
        } catch (Exception e) {
            System.err.println("Error occurred in getOrganizationById");
            e.printStackTrace();
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    @GetMapping("/{organizationId}/bloodSupplies")
    public ResponseEntity<List<BloodSupplyDTO>> getBloodSuppliesForOrganization(@PathVariable Long organizationId) {
        try {
            System.out.println("Request received for getBloodSuppliesForOrganization: " + organizationId);

            List<BloodSupplyDTO> bloodSupplies = organizationService.getBloodSuppliesForOrganization(organizationId);

            if (bloodSupplies != null) {
                System.out.println("Returned blood supplies for organization ID " + organizationId + ": " + bloodSupplies.size() + " items");
                for (BloodSupplyDTO bloodSupply : bloodSupplies) {
                    System.out.println(bloodSupply);
                }
                return new ResponseEntity<>(bloodSupplies, HttpStatus.OK);
            } else {
                System.err.println("Blood supplies not found for organization ID: " + organizationId);
                return new ResponseEntity<>(HttpStatus.NOT_FOUND);
            }
        } catch (Exception e) {
            System.err.println("Error occurred in getBloodSuppliesForOrganization");
            e.printStackTrace();
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    @GetMapping("/{organizationId}/appointments")
    public ResponseEntity<List<AppointmentDTO>> getAvailableAppointmentsForOrganization(@PathVariable Long organizationId) {
        try {
            List<AppointmentDTO> appointments = organizationService.getAvailableAppointmentsForOrganization(organizationId);

            if (appointments != null) {
                return new ResponseEntity<>(appointments, HttpStatus.OK);
            } else {
                System.err.println("Appointments not found for organization ID: " + organizationId);
                return new ResponseEntity<>(HttpStatus.NOT_FOUND);
            }
        } catch (Exception e) {
            System.err.println("Error occurred in getAvailableAppointmentsForOrganization");
            e.printStackTrace();
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    private void checkAllowed(Long id, String username) {
        String orgAdminUsername = organizationService.fetch(id).getAdminUsername();
        if (!orgAdminUsername.equals(username)) {
            throw new RequestDeniedException(
                    "Only admin (" + orgAdminUsername + ") can edit/view this organization, not: " + username
            );
        }
    }
}
