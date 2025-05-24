import React, { useEffect, useState, useCallback } from 'react';

export default function MeetingList() {
  const [meetings, setMeetings] = useState([]);

  const loadMeetings = useCallback(() => {
    fetch(`${process.env.REACT_APP_API_BASE_URL}/meetings`)
      .then(res => res.json())
      .then(data => setMeetings(data.meetings || []))
      .catch(console.error);
  }, []);

  useEffect(() => {
    // початкове завантаження
    loadMeetings();

    // підписка на подію створення зустрічі
    const handler = () => loadMeetings();
    window.addEventListener('meetingCreated', handler);

    return () => {
      window.removeEventListener('meetingCreated', handler);
    };
  }, [loadMeetings]);

  const handleDelete = async id => {
    if (!window.confirm('Видалити зустріч?')) return;
    await fetch(`${process.env.REACT_APP_API_BASE_URL}/meetings/${id}`, { method: 'DELETE' });
    // локально видаляємо без перезапиту
    setMeetings(ms => ms.filter(m => m.id !== id));
  };

  return (
    <div className="mb-6 p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Meetings</h2>
      {meetings.length === 0 ? <p>No meetings.</p> : (
        <ul>
          {meetings.map(m => (
            <li key={m.id} className="mb-2 flex justify-between">
              <span>{m.topic} @ {new Date(m.start_time).toLocaleString()}</span>
              <button onClick={() => handleDelete(m.id)} className="text-red-500">
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
