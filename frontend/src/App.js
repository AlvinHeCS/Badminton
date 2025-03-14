import React, { useState } from 'react';
import './App.css';
import axios from 'axios';
import { FaSpinner } from 'react-icons/fa';

function App() {
  const [location, setLocation] = useState('');
  const [date, setDate] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [courts, setCourts] = useState('');
  const [filteredCourts, setFilteredCourts] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const [showError, setShowError] = useState(false);
  const [loading, setLoading] = useState(false);


  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!courts || !endTime || !location || !startTime || !date) {
      setShowError(true);
      setTimeout(() => setShowError(false), 300);
      return;
    }

    const [year, month, day] = date.split('-');
    setLoading(true);

    //REACT_APP_API_URL_DEV='http://127.0.0.1:5000/api/search'
    //REACT_APP_API_URL_PRD='https://badmintoncourtfinder-alvinhecs-a79051a03cbf.herokuapp.com/api/search'
    //FRONTEND='https://badminton-7yrl.onrender.com/api/search'
    try {
      const response = await axios.post('https://badminton-7yrl.onrender.com/api/search', {
        location,
        startTime,
        endTime,
        courts,
        month,
        day,
      });

      setFilteredCourts(response.data);
      setShowResults(true);
    } catch (error) {
      console.error('Error fetching courts:', error);
      setFilteredCourts([]);
      setShowResults(true);
    } finally {
      setLoading(false); 
    }
  };

  
  
  return (
    <div className="App">
      <header className="app-header">
        <div className="logo">Badminton Booking</div>
        <div className="email">Badmintonbookingcourt@gmail.com</div>
      </header>
      <main>
        <section className={`search-section ${showResults ? "results-view" : "initial-view"}`}>
          {!showResults && (
            <div className="img-container">
              <img src="/shuttleCock.png" alt="shuttleCock" className="styled-img" />
            </div>
          )}
          <h2>Find Your Court</h2>
          <form onSubmit={handleSubmit} className="search-form">
            <div className="input-group">
              {/* Location Dropdown */}
              <select
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className={showError && !location ? "jiggle" : ""}
              >
                <option value="" disabled>Select Location</option>
                <option value="(-33.901882, 151.200010)">Alexandria</option>
                <option value="(-33.849602, 151.032745)">Auburn</option>
                <option value="(-33.950031, 151.203033)">Botany</option>
                <option value="(-33.732717, 151.005101)">Castle Hill</option>
                <option value="(-33.867486, 151.130091)">Five Dock</option>
                <option value="(-33.834011, 151.011124)">Granville</option>
                <option value="(-33.736469, 150.958298)">Norwest</option>
                <option value="(-33.814892, 151.035355)">Rydalmere</option>
                <option value="(-33.776227, 150.932315)">Seven Hills</option>
                <option value="(-33.837865, 151.046680)">Silverwater</option>
                <option value="(-33.865341, 150.968246)">Yennora</option>
              </select>
  
              {/* Date Picker */}
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className={showError && !date ? "jiggle" : ""}

                min={new Date().toISOString().split("T")[0]}
                max={new Date(new Date().setMonth(new Date().getMonth() + 3))
                  .toISOString()
                  .split("T")[0]}
              />
  
              {/* Start Time Dropdown */}
              <select
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                className={`am-pm-select ${showError && !startTime ? "jiggle" : ""}`}
              >
                <option value="" disabled>Start Time</option>
                {[
                  "09:00AM",
                  "10:00AM",
                  "11:00AM",
                  "12:00PM",
                  "01:00PM",
                  "02:00PM",
                  "03:00PM",
                  "04:00PM",
                  "05:00PM",
                  "06:00PM",
                  "07:00PM",
                  "08:00PM",
                  "09:00PM",
                  "10:00PM",
                ].map((time) => (
                  <option key={time} value={time}>
                    {time}
                  </option>
                ))}
              </select>
  
              {/* End Time Dropdown */}
              <select
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
                className={`am-pm-select ${showError && !endTime ? "jiggle" : ""}`}
              >
                <option value="" disabled>End Time</option>
                {[
                  "10:00AM",
                  "11:00AM",
                  "12:00PM",
                  "01:00PM",
                  "02:00PM",
                  "03:00PM",
                  "04:00PM",
                  "05:00PM",
                  "06:00PM",
                  "07:00PM",
                  "08:00PM",
                  "09:00PM",
                  "10:00PM",
                  "11:00PM",
                ].map((time) => (
                  <option key={time} value={time}>
                    {time}
                  </option>
                ))}
              </select>
  
              {/* Number of Courts Input */}
              <input
                type="number"
                placeholder="Number of courts"
                value={courts}
                min="1"
                onChange={(e) => setCourts(e.target.value)}
                className={showError && !courts ? "jiggle" : ""}
              />
  
              {/* Search Button */}
              <div className="search-container">
                <button
                  type="submit"
                  disabled={loading}
                  className="search-button"
                >
                  {loading ? <FaSpinner className="spinner-icon" /> : "Search"}
                </button>
              </div>
            </div>
          </form>
  
          {/* Apology Text */}
          {loading && (
            <p className="loading-message">
              Sorry for the load times — currently the backend is being hosted on Render's free servers 🤗.
            </p>
          )}
  
          {/* Court Results */}
          {showResults && (
            <div className="court-results">
              <h3>Available Courts</h3>
              {filteredCourts.length > 0 ? (
                <div className="court-list">
                  {filteredCourts.map((court) => (
                    <div key={court.id} className="court-card">
                      <div className="court-image-container">
                        <img src={court.image} alt={court.location} className="court-image" />
                      </div>
                      <div className="court-info">
                        <div className="court-header">
                          <h4 className="court-title">{court.name}</h4>
                          <a
                            href={court.mapsURL}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="maps-link"
                          >
                            Maps
                          </a>
                        </div>
                        <p><strong>Address:</strong> {court.address}</p>
                        <p><strong>Courts Free:</strong> {court.courtNos}</p>
                        <p className="court-price">
                          <span className="price-label"><strong>Price:</strong></span> ${court.price}
                        </p>
                        <a
                          href={court.URL}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="cta-button"
                        >
                          Book Now
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p>No courts available.</p>
              )}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
