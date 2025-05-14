import React, { useState } from 'react';

export default function JoinMeeting() {
  const [meetingId, setMeetingId] = useState('');

  const handleJoin = async () => {
    if (!meetingId) {
      alert('Please enter a Meeting ID');
      return;
    }
    try {
      const resp = await fetch(
        `${process.env.REACT_APP_API_BASE_URL}/meetings`
      );
      const data = await resp.json();
      const meeting = (data.meetings || []).find(
        m => String(m.id) === meetingId
      );
      if (!meeting) {
        alert('Meeting not found.');
        return;
      }
      window.open(meeting.join_url, '_blank');
    } catch (err) {
      console.error('Error fetching meetings:', err);
      alert('Could not retrieve meeting info.');
    }
  };

  return (
    <div className="p-4 rounded shadow mb-6">
      <h2 className="text-xl font-semibold mb-2">Join Meeting</h2>
      <div className="flex">
        <input
          value={meetingId}
          onChange={e => setMeetingId(e.target.value)}
          placeholder="Meeting ID"
          className="border p-1 flex-grow"
        />
        <button
          onClick={handleJoin}
          className="bg-purple-500 text-white px-3 py-1 ml-2 rounded"
        >
          Join
        </button>
      </div>
    </div>
  );
}
