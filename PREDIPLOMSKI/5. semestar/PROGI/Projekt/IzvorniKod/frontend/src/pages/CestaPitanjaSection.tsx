import React, { useState } from 'react';
import '../styles/CestaPitanjaSection.css';

interface FAQData {
  question1: string;
  question2: string;
  question3: string;
  question4: string;
}

const CestaPitanjaSection: React.FC = () => {
  const [selectedFAQ, setSelectedFAQ] = useState<string | null>(null);
  const [selectedQuestion, setSelectedQuestion] = useState<keyof FAQData | null>(null);

  const faqData: FAQData = {
    question1: 'Before donating blood, it is not necessary to be on an empty stomach. Blood donation is an integral part of everyday human life, and on that day, a person should eat and drink as usual. You will feel better if you have a light meal a few hours before donating blood. We kindly ask you not to consume excessively fatty food and alcohol within 8 hours before blood donation because their components may be introduced into the patient through a blood transfusion and cause harm.',
    question2: 'Yes, if they have not been tattooed in the last 4 months.',
    question3: 'The body of an adult, weighing over 55 kg, has more than 4.5 liters of blood. On average, blood constitutes 12% of a person\'s body weight. The body can tolerate blood loss up to 15% without any accompanying effects. By donating 450 mL of blood, the body loses less than 10% of the total blood volume.',
    question4: 'The blood transfusion service of each country monitors the epidemiological situation in the country, tracks the living conditions of donors, and based on these indicators, determines how and with which tests to examine the blood of donors for the presence of infectious agents. Therefore, each country can only ensure the safety of blood and blood products obtained from blood donors within that country. According to the Regulation on Blood and Blood Components from December 16, 1998 (Official Gazette 14/99), Article 9, paragraph 2 stipulates that blood donors must be citizens of the Republic of Croatia.',
  };

  const handleFAQClick = (questionKey: keyof FAQData) => {
    if (selectedQuestion === questionKey) {
      setSelectedQuestion(null);
      setSelectedFAQ(null);
    } else {
      setSelectedQuestion(questionKey);
      setSelectedFAQ(faqData[questionKey]);
    }
  };

  return (
    <div id="cestaPitanja" className={`faq-container ${selectedQuestion ? 'clicked' : ''}`}>
          <p className="cestaP"><b>Frequently Asked Questions</b></p>
      <div className={`faq-item ${selectedQuestion === 'question1' ? 'active' : ''}`} onClick={() => handleFAQClick('question1')}>
        {selectedQuestion === 'question1' ? '▲' : '▼'} Is it necessary to be on an empty stomach before donation?
      </div>
      {selectedQuestion === 'question1' && (
        <div className="faq-dropdown">
          <p>{selectedFAQ}</p>
        </div>
      )}
      <div className={`faq-item ${selectedQuestion === 'question2' ? 'active' : ''}`} onClick={() => handleFAQClick('question2')}>
        {selectedQuestion === 'question2' ? '▲' : '▼'} Are individuals with tattoos allowed to donate blood?
      </div>
      {selectedQuestion === 'question2' && (
        <div className="faq-dropdown">
          <p>{selectedFAQ}</p>
        </div>
      )}
      <div className={`faq-item ${selectedQuestion === 'question3' ? 'active' : ''}`} onClick={() => handleFAQClick('question3')}>
        {selectedQuestion === 'question3' ? '▲' : '▼'} Why is only 50ml of blood donated?
      </div>
      {selectedQuestion === 'question3' && (
        <div className="faq-dropdown">
          <p>{selectedFAQ}</p>
        </div>
      )}
      <div className={`faq-item ${selectedQuestion === 'question4' ? 'active' : ''}`} onClick={() => handleFAQClick('question4')}>
        {selectedQuestion === 'question4' ? '▲' : '▼'} Why can't foreign citizens donate blood?
      </div>
      {selectedQuestion === 'question4' && (
        <div className="faq-dropdown">
          <p>{selectedFAQ}</p>
        </div>
      )}
    </div>
  );
};

export default CestaPitanjaSection;
