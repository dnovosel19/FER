import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import NotFound from "./pages/NotFound";
import { Login } from "./pages/Login";
import { Register } from "./pages/Register";
import { MainP } from "./pages/MainP";
import { Schedule } from "./pages/Schedule";
import Homepage from "./pages/Homepage";
import { RegisterOrganization } from "./pages/RegisterOrganization";
import OrganizationHomepage from "./pages/organizationHomepage";
import BloodSuppliesPage from "./pages/BloodSuppliesPage";
import ReservedDonations from "./pages/reservedDonations";
import PersonalInformationPage from "./pages/PersonalInformationPage";
import DonationHistoryPage from "./pages/DonationHistoryPage";

export function Router() {
  return (
    <BrowserRouter>
      <div>
        <Routes>
          <Route path="/" element={<MainP />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/homepage/:donorId" element={<Homepage />} />
          <Route path="/organizationHomepage/:organizationId" element={<OrganizationHomepage />} />
          <Route path="/registerOrganization" element={<RegisterOrganization />} />
          <Route path="/organization/:organizationId/bloodSupplies" element={<BloodSuppliesPage />} />
          <Route path="/reservedDonations/:donorId" element={<ReservedDonations />} />
          <Route path="/donationHistory/:donorId" element={<DonationHistoryPage />} />
          <Route path="/schedule" element={<Schedule />} />
          <Route path="/changeSettings/:donorId" element={<PersonalInformationPage />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}