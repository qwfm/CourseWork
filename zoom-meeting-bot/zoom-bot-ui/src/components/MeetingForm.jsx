import React, { useState } from 'react';

export default function MeetingForm() {
  const [topic, setTopic] = useState('');
  const [startTime, setStartTime] = useState('');
  const [duration, setDuration] = useState(30);

  const handleSubmit = async e => {
    e.preventDefault();
    const resp = await fetch(`${process.env.REACT_APP_API_BASE_URL}/meetings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, start_time: startTime, duration })
    });
    const data = await resp.json();
    alert(`Created meeting ID: ${data.id}`);
    setTopic(''); setStartTime(''); setDuration(30);
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6 p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Create Meeting</h2>
      <div className="mb-2">
        <label className="block">Topic</label>
        <input value={topic} onChange={e => setTopic(e.target.value)} className="border p-1 w-full" />
      </div>
      <div className="mb-2">
        <label className="block">Start Time (ISO)</label>
        <input value={startTime} onChange={e => setStartTime(e.target.value)} className="border p-1 w-full" />
      </div>
      <div className="mb-4">
        <label className="block">Duration (minutes)</label>
        <input type="number" value={duration} onChange={e => setDuration(e.target.value)} className="border p-1 w-full" />
      </div>
      <button type="submit" className="bg-blue-500 text-white px-3 py-1 rounded">Create</button>
    </form>
  );
}