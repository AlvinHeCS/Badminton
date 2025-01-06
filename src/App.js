import React, { useState } from 'react';
import './App.css';

const availableCourts = [
  { id: 1, location: 'Downtown', time: '08:00', price: '$20/hr', image: 'NBCAlexandria.jpg', url: 'https://nbc.yepbooking.com.au/' },
  { id: 2, location: 'Uptown', time: '09:00', price: '$25/hr', image: 'NBCAlexandria.jpg', url: 'https://nbc.yepbooking.com.au/' },
  { id: 3, location: 'Midtown', time: '10:00', price: '$22/hr', image: 'NBCAlexandria.jpg', url: 'https://nbc.yepbooking.com.au/' },
  { id: 4, location: 'Downtown', time: '10:00', price: '$20/hr', image: 'NBCAlexandria.jpg', url: 'https://nbc.yepbooking.com.au/' },
  { id: 5, location: 'Suburb', time: '08:00', price: '$18/hr', image: 'NBCAlexandria.jpg', url: 'https://nbc.yepbooking.com.au/' },
];

function App() {
  const [location, setLocation] = useState('');
  const [date, setDate] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [courts, setCourts] = useState(1);
  const [filteredCourts, setFilteredCourts] = useState([]);
  const [showResults, setShowResults] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();

    const filtered = availableCourts.filter((court) => {
      return (
        (location ? court.location.toLowerCase().includes(location.toLowerCase()) : true) &&
        (startTime ? court.time >= startTime : true) &&
        (endTime ? court.time <= endTime : true)
      );
    });

    setFilteredCourts(filtered);
    setShowResults(true);
  };

  return (
    <div className="App">
      <header>
        <h1>Badminton Court Booking</h1>
      </header>
      <main>
        <section>
          <h2>Find Your Court</h2>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Enter location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
            <select
              id="start-time"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
            >
              <option value="" disabled>
                Starting Time
              </option>
              <option value="08:00">08:00 AM</option>
              <option value="09:00">09:00 AM</option>
              <option value="10:00">10:00 AM</option>
            </select>
            <select
              id="end-time"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
            >
              <option value="" disabled>
                Ending Time
              </option>
              <option value="08:00">08:00 AM</option>
              <option value="09:00">09:00 AM</option>
              <option value="10:00">10:00 AM</option>
            </select>
            <select
              value={courts}
              onChange={(e) => setCourts(parseInt(e.target.value))}
            >
              <option value="1">1 Court</option>
              <option value="2">2 Courts</option>
              <option value="3">3 Courts</option>
            </select>
            <button type="submit">Search</button>
          </form>

          {showResults && (
            <div className="court-results">
              <h3>Available Courts</h3>
              {filteredCourts.length > 0 ? (
                <div className="court-list">
                  {filteredCourts.map((court) => (
                    <div key={court.id} className="court-card">
                      <div className="court-info">
                        <h4>{court.location}</h4>
                        <p>Time: {court.time}</p>
                        <p>Price: {court.price}</p>
                        <a href={court.url} target="_blank" rel="noopener noreferrer">Book Now</a>
                      </div>
                      <img src={court.image} alt={court.location} className="court-image-small" />
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

