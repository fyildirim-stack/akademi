import React from 'react';
import { Calendar, User } from 'lucide-react';
import './ScheduleTable.css';

const monthNames = {
  '10': 'Ekim',
  '11': 'Kasım',
  '12': 'Aralık',
  '01': 'Ocak',
  '02': 'Şubat',
  '03': 'Mart',
  '04': 'Nisan',
  '05': 'Mayıs',
  '06': 'Haziran',
  '07': 'Temmuz',
  '08': 'Ağustos',
  '09': 'Eylül'
};

const getMonthYear = (dateString) => {
  if (!dateString) return { key: 'Bilinmeyen', label: 'Bilinmeyen', num: 'default' };
  const parts = dateString.split('.');
  if (parts.length >= 3) {
    const month = parts[1];
    const year = parts[2];
    return {
      key: `${year}-${month}`,
      label: `${monthNames[month] || month} ${year}`,
      num: month
    };
  }
  return { key: 'Bilinmeyen', label: 'Bilinmeyen', num: 'default' };
};

const ScheduleTable = ({ schedule }) => {
  // Veriyi aylara göre grupla
  const groupedSchedule = schedule.reduce((acc, item) => {
    const monthInfo = getMonthYear(item.saturday_date);
    if (!acc[monthInfo.key]) {
      acc[monthInfo.key] = {
        label: monthInfo.label,
        num: monthInfo.num,
        items: []
      };
    }
    acc[monthInfo.key].items.push(item);
    return acc;
  }, {});

  // Grupları tarihe göre sırala
  const sortedMonths = Object.keys(groupedSchedule).sort();

  return (
    <div className="schedule-container fade-in-up">
      {sortedMonths.map((monthKey) => {
        const monthGroup = groupedSchedule[monthKey];
        return (
          <div key={monthKey} className={`month-section glass-panel month-border-${monthGroup.num}`}>
            <h2 className={`month-header text-color-${monthGroup.num}`}>
              {monthGroup.label}
            </h2>
            <div className="table-container">
              <table className="schedule-table">
                <thead>
                  <tr>
                    <th>Hafta</th>
                    <th>Cumartesi</th>
                    <th>Pazar</th>
                  </tr>
                </thead>
                <tbody>
                  {monthGroup.items.map((item, index) => {
                    const fieldsSplit = item.fields ? item.fields.split('\n') : [];
                    const ctsField = fieldsSplit.length > 0 ? fieldsSplit[0].replace('Cts: ', '').replace('Cts:', '').trim() : '';
                    const pazField = fieldsSplit.length > 1 ? fieldsSplit[1].replace('Paz: ', '').replace('Paz:', '').trim() : '';
                    
                    const teachersSplit = item.teachers ? item.teachers.split('\nPaz:') : [];
                    const ctsTeacher = teachersSplit.length > 0 ? teachersSplit[0].replace('Cts: ', '').replace('Cts:', '').trim() : '';
                    const pazTeacher = teachersSplit.length > 1 ? teachersSplit[1].trim() : '';

                    return (
                      <tr key={index} className={`month-${monthGroup.num}`}>
                        <td className="week-col">
                          <span className="week-badge">{item.week}</span>
                          <span className="hours">{item.planned_hours} Saat</span>
                        </td>
                        <td>
                          <div className="day-cell">
                            <span className="date"><Calendar size={14} /> {item.saturday_date}</span>
                            <span className="course">
                              {ctsField && ctsField !== 'Ara dönem' && ctsField !== 'Ders yok' && ctsField !== 'Resmî tatil' && ctsField !== '—' && (
                                <span className="inline-field-badge">{ctsField}</span>
                              )}
                              {item.saturday_course}
                            </span>
                            {ctsTeacher && ctsTeacher !== 'Ara dönem' && ctsTeacher !== 'Ders yok' && ctsTeacher !== '—' && (
                              <span className="teacher"><User size={14} /> {ctsTeacher}</span>
                            )}
                          </div>
                        </td>
                        <td>
                          <div className="day-cell">
                            <span className="date"><Calendar size={14} /> {item.sunday_date}</span>
                            <span className="course">
                              {pazField && pazField !== 'Ara dönem' && pazField !== 'Ders yok' && pazField !== 'Resmî tatil' && pazField !== '—' && (
                                <span className="inline-field-badge">{pazField}</span>
                              )}
                              {item.sunday_course}
                            </span>
                            {pazTeacher && pazTeacher !== 'Ara dönem' && pazTeacher !== 'Ders yok' && pazTeacher !== '—' && (
                              <span className="teacher"><User size={14} /> {pazTeacher}</span>
                            )}
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ScheduleTable;
