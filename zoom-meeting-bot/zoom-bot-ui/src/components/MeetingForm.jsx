import React, { useState } from 'react';

const MeetingForm = () => {
  const [topic, setTopic] = useState('');
  const [startTime, setStartTime] = useState('');
  const [duration, setDuration] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const isoDate = parseCustomDate(startTime);
    if (!isoDate) {
      alert('Неправильний формат дати. Використовуйте дд.мм.рррр гг:хх');
      return;
    }

    try {
      const resp = await fetch(`${process.env.REACT_APP_API_BASE_URL}/meetings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic,
          start_time: isoDate,
          duration: parseInt(duration, 10),
        }),
      });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();
      console.log('Зустріч створено:', data);
      alert('Зустріч створено!');
      window.dispatchEvent(new Event('meetingCreated'));

      setTopic('');
      setStartTime('');
      setDuration('');
    } catch (error) {
      console.error('Помилка при створенні зустрічі:', error);
      alert('Не вдалося створити зустріч. Перевірте консоль для деталей.');
    }
  };

  const parseCustomDate = (input) => {
    const regex = /^(\d{2})\.(\d{2})\.(\d{4}) (\d{2}):(\d{2})$/;
    const match = input.match(regex);
    if (!match) return null;

    const [ , day, month, year, hours, minutes ] = match;
    const date = new Date(year, month - 1, day, hours, minutes);
    return isNaN(date.getTime()) ? null : date.toISOString();
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Тема зустрічі:</label>
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Дата та час початку (дд.мм.рррр гг:хх):</label>
        <input
          type="text"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
          placeholder="23.05.2025 14:30"
          required
        />
      </div>
      <div>
        <label>Тривалість (хвилини):</label>
        <input
          type="number"
          min="1"
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
          required
        />
      </div>
      <button type="submit">Створити зустріч</button>
    </form>
  );
};

export default MeetingForm;
