import React, { useState, useEffect } from 'react';

export default function ChatForm() {
  const [mode, setMode] = useState('channel');            // ’channel’ або ’contact’
  const [to, setTo] = useState('');
  const [message, setMessage] = useState('');
  const [channels, setChannels] = useState([]);

  // Нові стани для планування
  const [schedule, setSchedule] = useState(false);
  const [scheduledTime, setScheduledTime] = useState('');

  useEffect(() => {
    async function loadChannels() {
      try {
        const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/channels`);
        const data = await res.json();
        setChannels(data.channels || []);
      } catch (err) {
        console.error('Помилка завантаження каналів:', err);
      }
    }
    loadChannels();
  }, []);

  const sendChat = async e => {
    e.preventDefault();
    if (!to.trim() || !message.trim()) {
      alert('Заповніть отримувача та текст повідомлення');
      return;
    }
    // Будуємо тіло запиту
    const payload = { to, message };
    if (schedule && scheduledTime) {
      // Перетворюємо з datetime-local (YYYY-MM-DDThh:mm) в ISO
      payload.schedule_time = new Date(scheduledTime).toISOString();
    }
    try {
      const resp = await fetch(`${process.env.REACT_APP_API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      alert('Повідомлення заплановане/відправлене!');
      setTo('');
      setMessage('');
      setSchedule(false);
      setScheduledTime('');
    } catch (err) {
      console.error('Помилка відправки:', err);
      alert('Не вдалося відправити повідомлення');
    }
  };

  return (
    <form onSubmit={sendChat} className="mb-6 p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Написати в чат</h2>

      {/* Режим: канал чи контакт */}
      <div className="mb-4">
        <label className="font-medium mr-4">
          <input
            type="radio"
            checked={mode === 'channel'}
            onChange={() => setMode('channel')}
          />{' '}
          Канал
        </label>
        <label className="font-medium">
          <input
            type="radio"
            checked={mode === 'contact'}
            onChange={() => setMode('contact')}
          />{' '}
          Контакт
        </label>
      </div>

      {/* Отримувач */}
      {mode === 'channel' ? (
        <div className="mb-4">
          <label className="block mb-1 font-medium">Оберіть канал</label>
          <select
            value={to}
            onChange={e => setTo(e.target.value)}
            className="border p-2 w-full"
            required
          >
            <option value="">— виберіть канал —</option>
            {channels.map(ch => (
              <option key={ch.id} value={ch.jid}>
                {ch.name} (ID: {ch.id})
              </option>
            ))}
          </select>
        </div>
      ) : (
        <div className="mb-4">
          <label className="block mb-1 font-medium">JID користувача</label>
          <input
            type="text"
            value={to}
            onChange={e => setTo(e.target.value)}
            placeholder="user@xmpp.zoom.us"
            className="border p-2 w-full"
            required
          />
        </div>
      )}

      {/* Текст повідомлення */}
      <div className="mb-4">
        <label className="block mb-1 font-medium">Повідомлення</label>
        <textarea
          value={message}
          onChange={e => setMessage(e.target.value)}
          rows="4"
          className="border p-2 w-full"
          placeholder="Введіть текст..."
          required
        />
      </div>

      {/* Опція планування */}
      <div className="mb-4 flex items-center">
        <input
          type="checkbox"
          id="schedule"
          checked={schedule}
          onChange={e => setSchedule(e.target.checked)}
          className="mr-2"
        />
        <label htmlFor="schedule" className="font-medium">
          Запланувати відправлення
        </label>
      </div>
      {schedule && (
        <div className="mb-4">
          <label className="block mb-1 font-medium">
            Час відправлення
          </label>
          <input
            type="datetime-local"
            value={scheduledTime}
            onChange={e => setScheduledTime(e.target.value)}
            className="border p-2 w-full"
            required
          />
        </div>
      )}

      <button
        type="submit"
        className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
      >
        {schedule ? 'Запланувати' : 'Відправити'}
      </button>
    </form>
  );
}
